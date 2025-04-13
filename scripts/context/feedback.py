import os
import re
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

from .utils import (
    setup_logger, 
    ensure_dir, 
    extract_module_name, 
    read_file_content,
    write_json,
    read_json
)

class ContextFeedback:
    """
    A class to track and manage feedback on AI context modules.
    Uses SQLite to store feedback and optimization history.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the ContextFeedback system.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger = setup_logger('context_feedback')
        
        # Import optimizer for configuration access
        from .optimizer import ContextOptimizer
        self.optimizer = ContextOptimizer(config_path)
        self.config = self.optimizer.config
        
        # Set up database
        db_path = self.config.get('feedback_db', 'data/feedback.db')
        ensure_dir(os.path.dirname(db_path))
        self.db_path = db_path
        
        self._init_database()
        self.logger.info(f"ContextFeedback initialized with database: {db_path}")
    
    def _init_database(self):
        """
        Initialize the SQLite database with required tables.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create feedback table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS module_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_id TEXT,
                    feedback_type TEXT NOT NULL,
                    feedback_text TEXT,
                    effectiveness INTEGER,
                    target_model TEXT
                )
                ''')
                
                # Create optimization history table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS optimization_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    improvement REAL,
                    success INTEGER NOT NULL,
                    error_message TEXT,
                    diff_path TEXT
                )
                ''')
                
                conn.commit()
                self.logger.info("Database tables initialized")
                
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {str(e)}")
            raise
    
    def record_feedback(
        self,
        module_name: str,
        feedback_type: str,
        effectiveness: Optional[int] = None,
        feedback_text: Optional[str] = None,
        user_id: Optional[str] = None,
        target_model: Optional[str] = None
    ) -> Dict:
        """
        Record feedback for a context module.
        
        Args:
            module_name: Name of the module
            feedback_type: Type of feedback (e.g., 'effective', 'ineffective', 'error')
            effectiveness: Rating from 1 to 10
            feedback_text: Additional feedback text
            user_id: Identifier for the user providing feedback
            target_model: The AI model the feedback applies to
            
        Returns:
            dict: Result of the operation
        """
        try:
            timestamp = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO module_feedback 
                    (module_name, timestamp, user_id, feedback_type, feedback_text, effectiveness, target_model)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (module_name, timestamp, user_id, feedback_type, feedback_text, effectiveness, target_model)
                )
                conn.commit()
                feedback_id = cursor.lastrowid
            
            self.logger.info(f"Recorded feedback for module '{module_name}' (ID: {feedback_id})")
            return {
                "success": True,
                "feedback_id": feedback_id,
                "module_name": module_name,
                "timestamp": timestamp
            }
            
        except sqlite3.Error as e:
            error_msg = f"Error recording feedback: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def record_optimization(
        self,
        module_name: str,
        model_used: str,
        improvement: float,
        success: bool,
        error_message: Optional[str] = None,
        diff_path: Optional[str] = None
    ) -> Dict:
        """
        Record an optimization attempt for a module.
        
        Args:
            module_name: Name of the module
            model_used: AI model used for optimization
            improvement: Improvement percentage
            success: Whether the optimization was successful
            error_message: Error message if optimization failed
            diff_path: Path to the diff file
            
        Returns:
            dict: Result of the operation
        """
        try:
            timestamp = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO optimization_history 
                    (module_name, timestamp, model_used, improvement, success, error_message, diff_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (module_name, timestamp, model_used, improvement, 1 if success else 0, error_message, diff_path)
                )
                conn.commit()
                optimization_id = cursor.lastrowid
            
            self.logger.info(f"Recorded optimization for module '{module_name}' (ID: {optimization_id})")
            return {
                "success": True,
                "optimization_id": optimization_id,
                "module_name": module_name,
                "timestamp": timestamp
            }
            
        except sqlite3.Error as e:
            error_msg = f"Error recording optimization: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def get_module_feedback(self, module_name: Optional[str] = None, limit: int = 100) -> Dict:
        """
        Get feedback for a specific module or all modules.
        
        Args:
            module_name: Name of the module (None for all modules)
            limit: Maximum number of records to return
            
        Returns:
            dict: Feedback records
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if module_name:
                    query = "SELECT * FROM module_feedback WHERE module_name = ? ORDER BY timestamp DESC LIMIT ?"
                    cursor.execute(query, (module_name, limit))
                else:
                    query = "SELECT * FROM module_feedback ORDER BY timestamp DESC LIMIT ?"
                    cursor.execute(query, (limit,))
                
                rows = cursor.fetchall()
                feedback = [dict(row) for row in rows]
                
                return {
                    "success": True,
                    "count": len(feedback),
                    "feedback": feedback
                }
                
        except sqlite3.Error as e:
            error_msg = f"Error retrieving feedback: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def get_optimization_history(self, module_name: Optional[str] = None, limit: int = 100) -> Dict:
        """
        Get optimization history for a specific module or all modules.
        
        Args:
            module_name: Name of the module (None for all modules)
            limit: Maximum number of records to return
            
        Returns:
            dict: Optimization history records
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                if module_name:
                    query = "SELECT * FROM optimization_history WHERE module_name = ? ORDER BY timestamp DESC LIMIT ?"
                    cursor.execute(query, (module_name, limit))
                else:
                    query = "SELECT * FROM optimization_history ORDER BY timestamp DESC LIMIT ?"
                    cursor.execute(query, (limit,))
                
                rows = cursor.fetchall()
                history = [dict(row) for row in rows]
                
                return {
                    "success": True,
                    "count": len(history),
                    "history": history
                }
                
        except sqlite3.Error as e:
            error_msg = f"Error retrieving optimization history: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def get_module_effectiveness(self, module_name: Optional[str] = None, target_model: Optional[str] = None) -> Dict:
        """
        Calculate the effectiveness of modules based on feedback.
        
        Args:
            module_name: Name of the module (None for all modules)
            target_model: Filter by specific model
            
        Returns:
            dict: Module effectiveness data
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Construct the query based on parameters
                query = """
                SELECT 
                    module_name,
                    COUNT(*) as feedback_count,
                    AVG(effectiveness) as avg_effectiveness,
                    SUM(CASE WHEN feedback_type = 'effective' THEN 1 ELSE 0 END) as effective_count,
                    SUM(CASE WHEN feedback_type = 'ineffective' THEN 1 ELSE 0 END) as ineffective_count,
                    SUM(CASE WHEN feedback_type = 'error' THEN 1 ELSE 0 END) as error_count
                FROM module_feedback
                """
                
                params = []
                where_clauses = []
                
                if module_name:
                    where_clauses.append("module_name = ?")
                    params.append(module_name)
                
                if target_model:
                    where_clauses.append("target_model = ?")
                    params.append(target_model)
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
                
                query += " GROUP BY module_name ORDER BY avg_effectiveness ASC"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                effectiveness_data = []
                for row in rows:
                    row_dict = dict(row)
                    
                    # Calculate effectiveness percentage
                    if row_dict['feedback_count'] > 0:
                        row_dict['effectiveness_percent'] = (row_dict['effective_count'] / row_dict['feedback_count']) * 100
                    else:
                        row_dict['effectiveness_percent'] = 0
                    
                    effectiveness_data.append(row_dict)
                
                return {
                    "success": True,
                    "count": len(effectiveness_data),
                    "modules": effectiveness_data
                }
                
        except sqlite3.Error as e:
            error_msg = f"Error calculating module effectiveness: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def get_modules_for_optimization(
        self, 
        min_feedback: int = 5, 
        max_effectiveness: float = 70.0,
        target_model: Optional[str] = None,
        limit: int = 10
    ) -> Dict:
        """
        Get a list of modules that would benefit from optimization.
        
        Args:
            min_feedback: Minimum number of feedback entries to consider
            max_effectiveness: Maximum effectiveness percentage to consider for optimization
            target_model: Filter for specific model
            limit: Maximum number of modules to return
            
        Returns:
            dict: List of modules for optimization
        """
        try:
            effectiveness_data = self.get_module_effectiveness(target_model=target_model)
            
            if not effectiveness_data.get("success", False):
                return effectiveness_data
            
            # Filter modules based on criteria
            candidates = []
            for module in effectiveness_data["modules"]:
                if (module["feedback_count"] >= min_feedback and 
                    module["effectiveness_percent"] <= max_effectiveness):
                    candidates.append(module)
            
            # Sort by effectiveness (ascending) and feedback count (descending)
            candidates.sort(key=lambda x: (x["effectiveness_percent"], -x["feedback_count"]))
            
            # Limit the number of results
            candidates = candidates[:limit]
            
            return {
                "success": True,
                "count": len(candidates),
                "modules": candidates
            }
            
        except Exception as e:
            error_msg = f"Error identifying modules for optimization: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def calculate_optimization_success_rate(self, threshold: float = 5.0) -> Dict:
        """
        Calculate the success rate of module optimizations.
        
        Args:
            threshold: Improvement percentage threshold to consider an optimization successful
            
        Returns:
            dict: Optimization success statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get total optimization attempts
                cursor.execute("SELECT COUNT(*) as total FROM optimization_history WHERE success = 1")
                total = cursor.fetchone()["total"]
                
                # Get successful optimizations (above threshold)
                cursor.execute(
                    "SELECT COUNT(*) as count FROM optimization_history WHERE success = 1 AND improvement >= ?",
                    (threshold,)
                )
                successful = cursor.fetchone()["count"]
                
                # Get optimizations that resulted in regression
                cursor.execute(
                    "SELECT COUNT(*) as count FROM optimization_history WHERE success = 1 AND improvement < 0",
                    ()
                )
                regression = cursor.fetchone()["count"]
                
                # Get failed optimization attempts
                cursor.execute("SELECT COUNT(*) as count FROM optimization_history WHERE success = 0")
                failed = cursor.fetchone()["count"]
                
                # Calculate success rate
                success_rate = (successful / total * 100) if total > 0 else 0
                
                return {
                    "success": True,
                    "total_optimizations": total,
                    "successful_optimizations": successful,
                    "regression_count": regression,
                    "failed_attempts": failed,
                    "success_rate": success_rate,
                    "threshold": threshold
                }
                
        except sqlite3.Error as e:
            error_msg = f"Error calculating optimization success rate: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def export_data(self, output_path: Optional[str] = None) -> Dict:
        """
        Export feedback and optimization data to a JSON file.
        
        Args:
            output_path: Path to save the exported data
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Default output path
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"data/exports/feedback_export_{timestamp}.json"
            
            # Create directory if it doesn't exist
            ensure_dir(os.path.dirname(output_path))
            
            # Get feedback and optimization data
            feedback_data = self.get_module_feedback(limit=1000)
            optimization_data = self.get_optimization_history(limit=1000)
            
            if not feedback_data.get("success", False) or not optimization_data.get("success", False):
                error_msg = "Failed to retrieve data for export"
                self.logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # Prepare export data
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "feedback": feedback_data.get("feedback", []),
                "optimization_history": optimization_data.get("history", []),
                "summary": {
                    "total_feedback": len(feedback_data.get("feedback", [])),
                    "total_optimizations": len(optimization_data.get("history", [])),
                    "avg_improvement": self._calculate_avg_improvement(optimization_data.get("history", []))
                }
            }
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Data exported to {output_path}")
            return {
                "success": True,
                "output_path": output_path,
                "record_count": export_data["summary"]["total_feedback"] + export_data["summary"]["total_optimizations"]
            }
            
        except Exception as e:
            error_msg = f"Error exporting data: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def _calculate_avg_improvement(self, history: List[Dict]) -> float:
        """
        Calculate the average improvement from optimization history.
        
        Args:
            history: List of optimization history records
            
        Returns:
            float: Average improvement percentage
        """
        if not history:
            return 0.0
        
        # Filter out failed optimizations
        successful = [h for h in history if h.get("success") == 1]
        
        if not successful:
            return 0.0
        
        # Calculate average improvement
        total_improvement = sum(h.get("improvement", 0) for h in successful)
        return total_improvement / len(successful) 