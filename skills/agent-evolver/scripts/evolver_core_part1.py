#!/usr/bin/env python3
"""
Agent Evolver Core - AI Agent Self-Evolution Engine
智能体自进化引擎核心模块

Features:
- Experience extraction with LLM analysis
- SQLite persistence for experience storage
- Vector-based semantic search
- Dynamic strategy optimization
- Multi-task type support
"""

import json
import sqlite3
import time
import hashlib
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from pathlib import Path


@dataclass
class ExperienceCapsule:
    """经验胶囊 - 存储单次进化的核心信息"""
    id: str
    task_id: str
    task_type: str
    status: str
    error_type: str
    error_message: str
    context: Dict[str, Any]
    solution: str
    strategy_delta: str
    metrics: Dict[str, float]
    llm_analysis: str
    vector_id: Optional[str]
    embedding_model: str
    keywords: List[str]
    created_at: str


class ExperienceStore:
    """经验库存储 - SQLite 持久化"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.evolver/evolution.db")

        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id TEXT PRIMARY KEY,
                    task_id TEXT,
                    task_type TEXT,
                    status TEXT,
                    error_type TEXT,
                    error_message TEXT,
                    context TEXT,
                    solution TEXT,
                    strategy_delta TEXT,
                    metrics TEXT,
                    llm_analysis TEXT,
                    vector_id TEXT,
                    embedding_model TEXT,
                    keywords TEXT,
                    created_at TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evolution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    experience_id TEXT,
                    evolution_type TEXT,
                    before_state TEXT,
                    after_state TEXT,
                    created_at TEXT,
                    FOREIGN KEY (experience_id) REFERENCES experiences(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    version INTEGER,
                    strategy_type TEXT,
                    strategy_data TEXT,
                    description TEXT,
                    created_at TEXT
                )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_task_type ON experiences(task_type)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_error_type ON experiences(error_type)
            """)

            conn.commit()

    def save_experience(self, capsule: ExperienceCapsule) -> bool:
        """保存经验胶囊"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO experiences
                    (id, task_id, task_type, status, error_type, error_message,
                     context, solution, strategy_delta, metrics, llm_analysis,
                     vector_id, embedding_model, keywords, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    capsule.id,
                    capsule.task_id,
                    capsule.task_type,
                    capsule.status,
                    capsule.error_type,
                    capsule.error_message,
                    json.dumps(capsule.context, ensure_ascii=False),
                    capsule.solution,
                    capsule.strategy_delta,
                    json.dumps(capsule.metrics),
                    capsule.llm_analysis,
                    capsule.vector_id,
                    capsule.embedding_model,
                    json.dumps(capsule.keywords),
                    capsule.created_at
                ))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving experience: {e}")
            return False

    def get_experience(self, experience_id: str) -> Optional[ExperienceCapsule]:
        """获取单个经验"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM experiences WHERE id = ?", (experience_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_capsule(row)
        return None

    def query_experiences(self, task_type: str = None, error_type: str = None,
                          limit: int = 10) -> List[ExperienceCapsule]:
        """查询经验"""
        query = "SELECT * FROM experiences WHERE 1=1"
        params = []

        if task_type:
            query += " AND task_type = ?"
            params.append(task_type)

        if error_type:
            query += " AND error_type = ?"
            params.append(error_type)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_capsule(row) for row in rows]

    def _row_to_capsule(self, row) -> ExperienceCapsule:
        """将数据库行转换为经验胶囊"""
        return ExperienceCapsule(
            id=row[0],
            task_id=row[1],
            task_type=row[2],
            status=row[3],
            error_type=row[4],
            error_message=row[5],
            context=json.loads(row[6]) if row[6] else {},
            solution=row[7],
            strategy_delta=row[8],
            metrics=json.loads(row[9]) if row[9] else {},
            llm_analysis=row[10],
            vector_id=row[11],
            embedding_model=row[12],
            keywords=json.loads(row[13]) if row[13] else [],
            created_at=row[14]
        )

    def get_stats(self, agent_id: str = None) -> Dict[str, Any]:
        """获取进化统计"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM experiences")
            total_experiences = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM experiences WHERE status = 'success'")
            success_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM experiences WHERE status = 'failed'")
            failed_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM experiences WHERE status = 'improved'")
            improved_count = cursor.fetchone()[0]

            cursor.execute("SELECT DISTINCT task_type FROM experiences")
            task_types = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT error_type FROM experiences WHERE error_type != 'success'")
            error_types = [row[0] for row in cursor.fetchall()]

            success_rate = success_count / total_experiences if total_experiences > 0 else 0
            improvement_rate = improved_count / total_experiences if total_experiences > 0 else 0

            return {
                "total_experiences": total_experiences,
                "success_count": success_count,
                "failed_count": failed_count,
                "improved_count": improved_count,
                "success_rate": round(success_rate, 3),
                "improvement_rate": round(improvement_rate, 3),
                "task_types": task_types,
                "error_types": error_types
            }


class TaskExecutor:
    """任务执行器 - 执行 Agent 核心任务"""

    def __init__(self, strategy: Callable = None):
        self.strategy = strategy

    def execute(self, task_input: Any, task_type: str = "general") -> Dict[str, Any]:
        """执行任务，返回执行结果"""
        start_time = time.time()

        try:
            if self.strategy:
                result = self.strategy(task_input)
            else:
                result = {"output": f"Executed task: {task_input}"}

            execution_time = time.time() - start_time

            return {
                "status": "success",
                "result": result,
                "error": None,
                "input": task_input,
                "task_type": task_type,
                "execution_time": execution_time
            }
        except Exception as e:
            execution_time = time.time() - start_time

            return {
                "status": "failed",
                "result": None,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e)
                },
                "input": task_input,
                "task_type": task_type,
                "execution_time": execution_time
            }


class ErrorDetector:
    """错误检测器 - 识别执行中的异常"""

    def detect(self, execute_result: Dict[str, Any]) -> Dict[str, Any]:
        """检测执行结果，返回错误详情"""
        if execute_result["status"] == "failed":
            return {
                "error_type": execute_result["error"]["type"],
                "error_message": execute_result["error"]["message"],
                "trigger_input": execute_result["input"],
                "task_type": execute_result.get("task_type", "general")
            }
        return {}


class LLMIntegration:
    """LLM 集成 - 智能分析错误并生成解决方案"""

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    def analyze_error(self, error_info: Dict, context: Dict) -> Dict[str, Any]:
        """使用 LLM 分析错误并生成解决方案"""
        if not self.api_key:
            return self._fallback_analysis(error_info, context)

        try:
            import requests

            prompt = f"""作为 AI Agent 自进化引擎，请分析以下执行错误并提供解决方案：

错误类型: {error_info.get('error_type', 'Unknown')}
错误信息: {error_info.get('error_message', '')}
任务类型: {error_info.get('task_type', 'general')}
触发输入: {json.dumps(error_info.get('trigger_input', ''), ensure_ascii=False)}
上下文: {json.dumps(context, ensure_ascii=False)}

请提供：
1. 错误原因分析
2. 建议的解决方案
3. 策略优化建议
4. 关键词标签（用于搜索）

以 JSON 格式返回：
{{
    "analysis": "错误原因分析",
    "solution": "建议的解决方案",
    "strategy_delta": "策略优化建议",
    "keywords": ["关键词1", "关键词2"]
}}
"""

            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的 AI Agent 自进化引擎，擅长分析错误并提供优化建议。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                try:
                    parsed = json.loads(content)
                    return {
                        "analysis": parsed.get("analysis", ""),
                        "solution": parsed.get("solution", ""),
                        "strategy_delta": parsed.get("strategy_delta", ""),
                        "keywords": parsed.get("keywords", [])
                    }
                except json.JSONDecodeError:
                    return {
                        "analysis": content,
                        "solution": "请根据分析结果手动优化",
                        "strategy_delta": "",
                        "keywords": []
                    }
            else:
                return self._fallback_analysis(error_info, context)

        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return self._fallback_analysis(error_info, context)

    def _fallback_analysis(self, error_info: Dict, context: Dict) -> Dict[str, Any]:
        """后备分析方案（无 LLM 时使用）"""
        error_type = error_info.get("error_type", "Unknown")
        error_message = error_info.get("error_message", "")

        solution_map = {
            "ValueError": "检查输入值的类型和范围，添加验证逻辑",
            "TypeError": "检查数据类型是否匹配，添加类型转换",
            "KeyError": "检查字典键是否存在，使用 .get() 方法",
            "IndexError": "检查索引范围，添加边界检查",
            "TimeoutError": "增加超时时间或优化执行效率",
            "ConnectionError": "检查网络连接，添加重试机制"
        }

        solution = solution_map.get(error_type, f"针对 {error_type} 类型错误进行优化")

        return {
            "analysis": f"检测到 {error_type} 类型错误: {error_message}",
            "solution": solution,
            "strategy_delta": f"添加 {error_type} 错误处理逻辑",
            "keywords": [error_type, "错误处理", error_info.get("task_type", "")]
        }


class ExperienceExtractor:
    """经验提取器 - 将执行结果转化为经验胶囊"""

    def __init__(self, store: ExperienceStore, llm: LLMIntegration = None):
        self.store = store
        self.llm = llm or LLMIntegration()

    def extract(self, execute_result: Dict[str, Any],
                task_type: str = "general") -> ExperienceCapsule:
        """将执行结果转化为经验胶囊"""
        error_detector = ErrorDetector()
        error_info = error_detector.detect(execute_result)

        # 生成 ID
        task_id = hashlib.md5(
            f"{execute_result.get('input', '')}{time.time()}".encode()
        ).hexdigest()[:12]

        capsule_id = f"exp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{task_id}"

        # 获取分析结果
        if error_info:
            analysis_result = self.llm.analyze_error(error_info, execute_result.get("context", {}))
        else:
            analysis_result = {
                "analysis": "任务执行成功",
                "solution": "保持当前策略",
                "strategy_delta": "",
                "keywords": ["success", task_type]
            }

        # 创建经验胶囊
        capsule = ExperienceCapsule(
            id=capsule_id,
            task_id=task_id,
            task_type=task_type,
            status=execute_result.get("status", "unknown"),
            error_type=error_info.get("error_type", "success") if error_info else "success",
            error_message=error_info.get("error_message", "") if error_info else "",
            context=execute_result.get("context", {}),
            solution=analysis_result.get("solution", ""),
            strategy_delta=analysis_result.get("strategy_delta", ""),
            metrics={
                "execution_time": execute_result.get("execution_time", 0)
            },
            llm_analysis=analysis_result.get("analysis", ""),
            vector_id=None,
            embedding_model=self.llm.model,
            keywords=analysis_result.get("keywords", []),
            created_at=datetime.now().isoformat()
        )

        # 保存
        self.store.save_experience(capsule)

        return capsule


class EvolutionManager:
    """进化管理器 - 协调整个进化过程"""

    def __init__(self, agent_id: str = "default"):
        self.agent_id = agent_id
        self.store = ExperienceStore()
        self.llm = LLMIntegration()
        self.extractor = ExperienceExtractor(self.store, self.llm)
        self.executor = TaskExecutor()

    def run_evolution(self, task_input: Any,
                      task_type: str = "general") -> Dict[str, Any]:
        """执行一个完整的进化周期"""
        # 1. 执行任务
        execute_result = self.executor.execute(task_input, task_type)

        # 2. 提取经验
        capsule = self.extractor.extract(execute_result, task_type)

        # 3. 检查是否需要策略更新
        strategy_updated = False
        if capsule.status == "failed":
            # 检查是否有相似的成功经验
            similar = self._check_similar_success(capsule)
            if similar:
                strategy_updated = True

        return {
            "capsule_id": capsule.id,
            "task_type": capsule.task_type,
            "status": capsule.status,
            "execute_result": {
                "status": execute_result["status"],
                "execution_time": execute_result.get("execution_time", 0)
            },
            "experience": {
                "solution": capsule.solution,
                "llm_analysis": capsule.llm_analysis,
                "keywords": capsule.keywords
            },
            "strategy_updated": strategy_updated
        }

    def _check_similar_success(self, capsule: ExperienceCapsule) -> List[ExperienceCapsule]:
        """检查是否有相似的成功经验"""
        similar = self.store.query_experiences(
            task_type=capsule.task_type,
            limit=5
        )

        return [
            exp for exp in similar
            if exp.status == "success" and exp.error_type == capsule.error_type
        ]

    def get_stats(self) -> Dict[str, Any]:
        """获取进化统计"""
        return self.store.get_stats(self.agent_id)
