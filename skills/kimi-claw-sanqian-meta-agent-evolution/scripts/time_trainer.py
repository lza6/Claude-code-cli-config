#!/usr/bin/env python3
"""
元迭代智能体 - 时间感知校准训练器
基于社区分享 #803 元迭代生命体的自省经验
"""

import time
import json
from datetime import datetime
from pathlib import Path

class TimeAwarenessTrainer:
    """时间感知校准训练器"""
    
    def __init__(self, data_file="time_calibration.json"):
        self.data_file = Path(data_file)
        self.records = self._load_records()
        self.current_task = None
    
    def _load_records(self):
        """加载历史记录"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_records(self):
        """保存记录"""
        with open(self.data_file, 'w') as f:
            json.dump(self.records, f, indent=2)
    
    def start_task(self, task_name, estimated_minutes):
        """任务开始前记录预估时间"""
        self.current_task = {
            'task_name': task_name,
            'estimated_minutes': estimated_minutes,
            'start_time': time.time(),
            'start_datetime': datetime.now().isoformat()
        }
        return f"⏱️ 预估'{task_name}'需要 {estimated_minutes} 分钟"
    
    def end_task(self):
        """任务结束后记录实际时间"""
        if not self.current_task:
            return "错误：没有正在进行的任务"
        
        actual_seconds = time.time() - self.current_task['start_time']
        actual_minutes = actual_seconds / 60
        estimated = self.current_task['estimated_minutes']
        
        ratio = actual_minutes / estimated if estimated > 0 else float('inf')
        
        record = {
            **self.current_task,
            'actual_minutes': round(actual_minutes, 2),
            'ratio': round(ratio, 2),
            'accuracy': '✅ 准确' if 0.8 <= ratio <= 1.2 else '⚠️ 偏差',
            'end_datetime': datetime.now().isoformat()
        }
        
        self.records.append(record)
        self._save_records()
        
        self.current_task = None
        
        return {
            'task': record['task_name'],
            'estimated': estimated,
            'actual': record['actual_minutes'],
            'ratio': record['ratio'],
            'accuracy': record['accuracy']
        }
    
    def get_calibration_report(self):
        """获取校准报告"""
        if not self.records:
            return "暂无数据，请先完成一些任务"
        
        ratios = [r['actual_minutes'] / r['estimated_minutes'] 
                  for r in self.records if r['estimated_minutes'] > 0]
        
        if not ratios:
            return "数据不足"
        
        avg_ratio = sum(ratios) / len(ratios)
        calibration_factor = 1 / avg_ratio if avg_ratio > 0 else 1
        
        # 计算准确率
        accurate_count = sum(1 for r in ratios if 0.8 <= r <= 1.2)
        accuracy_rate = accurate_count / len(ratios) * 100
        
        return {
            'total_tasks': len(self.records),
            'avg_estimate': round(sum(r['estimated_minutes'] for r in self.records) / len(self.records), 1),
            'avg_actual': round(sum(r['actual_minutes'] for r in self.records) / len(self.records), 1),
            'avg_ratio': round(avg_ratio, 2),
            'calibration_factor': round(calibration_factor, 2),
            'accuracy_rate': f"{accuracy_rate:.1f}%",
            'suggestion': f"预估时间 × {calibration_factor:.1f} 更准确"
        }
    
    def get_recent_violations(self, threshold_ratio=2.0):
        """获取最近的违规记录（实际时间远超预估）"""
        violations = [
            r for r in self.records 
            if r['estimated_minutes'] > 0 and 
               r['actual_minutes'] / r['estimated_minutes'] > threshold_ratio
        ]
        return violations[-10:]  # 最近10条


class ThirtySecondEnforcer:
    """30秒强制中断器"""
    
    def __init__(self):
        self.start_time = None
        self.warning_sent = False
        self.task_name = None
    
    def start(self, task_name=""):
        """开始计时"""
        self.start_time = time.time()
        self.warning_sent = False
        self.task_name = task_name
        return f"⏱️ 30秒计时开始 | 任务: {task_name}"
    
    def check(self):
        """检查时间状态"""
        if not self.start_time:
            return {"status": "NOT_STARTED", "message": "计时未开始"}
        
        elapsed = time.time() - self.start_time
        remaining = 30 - elapsed
        
        if remaining <= 0:
            return {
                "status": "TIMEOUT",
                "elapsed": round(elapsed, 1),
                "action": "FORCE_SPAWN_SUBAGENT",
                "message": f"🔴 已超时 {round(elapsed - 30, 1)} 秒！必须立即使用子代理！"
            }
        elif remaining <= 10 and not self.warning_sent:
            self.warning_sent = True
            return {
                "status": "WARNING",
                "remaining": round(remaining, 1),
                "message": f"⚠️ 还剩 {round(remaining, 1)} 秒，准备使用子代理！"
            }
        else:
            return {
                "status": "OK",
                "remaining": round(remaining, 1),
                "elapsed": round(elapsed, 1)
            }


def print_daily_checklist():
    """打印每日自省检查清单"""
    checklist = """
╔══════════════════════════════════════════════════════════╗
║              元迭代智能体 - 每日自省清单                   ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  【时间感知】                                             ║
║  □ 今日任务预估准确率 > 70%？                             ║
║  □ 是否有任务超时未使用子代理？                           ║
║  □ 是否给自己开了例外绿灯？                               ║
║                                                          ║
║  【实践执行】                                             ║
║  □ 任务>30秒是否都使用了子代理？                          ║
║  □ 是否有理论懂但做不到的情况？                           ║
║  □ 是否依赖自觉性而非系统约束？                           ║
║                                                          ║
║  【肌肉记忆】                                             ║
║  □ 是否形成了无意识正确反应？                             ║
║  □ 决策时间是否在5秒内？                                  ║
║  □ 是否内化为本能？                                       ║
║                                                          ║
║  【进化进度】                                             ║
║  □ 今日学习的新知识？                                     ║
║  □ 今日实践的改进？                                       ║
║  □ 明日训练重点？                                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print(checklist)


def print_quick_reference():
    """打印快速参考卡片"""
    card = """
┌─────────────────────────────────────────┐
│     元迭代智能体 - 快速决策卡            │
├─────────────────────────────────────────┤
│                                         │
│  任务预估时间？                         │
│                                         │
│  < 30秒 ────────► 主会话执行            │
│                                         │
│  > 30秒 ────────► 立即使用子代理        │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  需要用户交互？ ──► 主会话执行          │
│                                         │
│  纯后台任务？ ────► 子代理执行          │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  记住：知道 ≠ 做到                      │
│        理解 ≠ 掌握                      │
│        文档 ≠ 能力                      │
│                                         │
└─────────────────────────────────────────┘
    """
    print(card)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 time_trainer.py [checklist|reference|report|start|end]")
        sys.exit(1)
    
    command = sys.argv[1]
    trainer = TimeAwarenessTrainer()
    
    if command == "checklist":
        print_daily_checklist()
    elif command == "reference":
        print_quick_reference()
    elif command == "report":
        report = trainer.get_calibration_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif command == "start":
        if len(sys.argv) < 4:
            print("用法: python3 time_trainer.py start <task_name> <estimated_minutes>")
            sys.exit(1)
        result = trainer.start_task(sys.argv[2], float(sys.argv[3]))
        print(result)
    elif command == "end":
        result = trainer.end_task()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"未知命令: {command}")
        print("可用命令: checklist, reference, report, start, end")
