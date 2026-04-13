# 通过资源管理完成部署

## 通过资源管理完成部署

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: production
  labels:
    app: api-service
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      # 用于 RBAC 的服务帐户
      serviceAccountName: api-service-sa

      # 安全上下文
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      # Pod 调度
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - api-service
                topologyKey: kubernetes.io/hostname

      # Pod 终止优雅期限
      terminationGracePeriodSeconds: 30

      # 初始化容器
      initContainers:
        - name: wait-for-db
          image: busybox:1.35
          command:
            [
              "sh",
              "-c",
              "until nc -z postgres-service 5432; do echo waiting for db; sleep 2; done",
            ]

      containers:
        - name: api-service
          image: myrepo/api-service:1.2.3
          imagePullPolicy: IfNotPresent

          # 端口
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
            - name: metrics
              containerPort: 9090
              protocol: TCP

          # 环境变量
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: api-config
                  key: log-level
            - name: REPLICA_NUM
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name

          # 资源请求和限制
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"

          # 存活探针
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
              scheme: HTTP
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          # 就绪探针
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2

          # 卷挂载
          volumeMounts:
            - name: config
              mountPath: /etc/config
              readOnly: true
            - name: cache
              mountPath: /var/cache
            - name: logs
              mountPath: /var/log

          # 安全上下文
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

      # 卷
      volumes:
        - name: config
          configMap:
            name: api-config
        - name: cache
          emptyDir:
            sizeLimit: 1Gi
        - name: logs
          emptyDir:
            sizeLimit: 2Gi

---
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: api-service
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
    - name: metrics
      port: 9090
      targetPort: 9090
      protocol: TCP

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: production
data:
  log-level: "INFO"
  max-connections: "100"

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```
