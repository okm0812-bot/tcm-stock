# (Continued from evolver_core_part1.py)
# This file contains the remaining classes for agent-evolver

class StrategyManager:
    """策略管理器 - 管理 Agent 策略版本"""

    def __init__(self, store: ExperienceStore, agent_id: str = "default"):
        self.store = store
        self.agent_id = agent_id

    def get_current_strategy(self, strategy_type: str = "general") -> Optional[Dict]:
        """获取当前策略"""
        with sqlite3.connect(self.store.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM strategies
                WHERE agent_id = ? AND strategy_type = ?
                ORDER BY version DESC LIMIT 1
            """, (self.agent_id, strategy_type))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "agent_id": row[1],
                    "version": row[2],
                    "strategy_type": row[3],
                    "strategy_data": json.loads(row[4]) if row[4] else {},
                    "description": row[5],
                    "created_at": row[6]
                }
        return None

    def save_strategy(self, strategy_type: str, strategy_data: Dict,
                     description: str = "") -> bool:
        """保存新策略版本"""
        try:
            with sqlite3.connect(self.store.db_path) as conn:
                cursor = conn.cursor()
                # 获取最新版本号
                cursor.execute("""
                    SELECT MAX(version) FROM strategies
                    WHERE agent_id = ? AND strategy_type = ?
                """, (self.agent_id, strategy_type))
                max_version = cursor.fetchone()[0] or 0

                cursor.execute("""
                    INSERT INTO strategies
                    (agent_id, version, strategy_type, strategy_data, description, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.agent_id,
                    max_version + 1,
                    strategy_type,
                    json.dumps(strategy_data, ensure_ascii=False),
                    description,
                    datetime.now().isoformat()
                ))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving strategy: {e}")
            return False

    def rollback(self, strategy_type: str, target_version: int) -> bool:
        """回滚到指定版本"""
        try:
            with sqlite3.connect(self.store.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM strategies
                    WHERE agent_id = ? AND strategy_type = ? AND version = ?
                """, (self.agent_id, strategy_type, target_version))
                row = cursor.fetchone()
                if not row:
                    return False

                # 创建新版本（复制目标版本）
                cursor.execute("""
                    SELECT MAX(version) FROM strategies
                    WHERE agent_id = ? AND strategy_type = ?
                """, (self.agent_id, strategy_type))
                max_version = cursor.fetchone()[0] or 0

                cursor.execute("""
                    INSERT INTO strategies
                    (agent_id, version, strategy_type, strategy_data, description, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.agent_id,
                    max_version + 1,
                    strategy_type,
                    row[4],
                    f"Rollback to version {target_version}",
                    datetime.now().isoformat()
                ))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error rolling back strategy: {e}")
            return False
