#!/usr/bin/env python3
"""
Context Module Feedback System

Tracks user feedback on context modules, stores data in SQLite,
and provides analysis to prioritize optimization efforts.
"""

import argparse
import json
import logging
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ContextFeedback")

class ContextFeedback:
    """
    Tracks and analyzes feedback data for context modules.
    Provides prioritization for optimization based on user feedback and performance metrics.
    """
    
    def __init__(self, db_path: str = "context_feedback.db"):
        """
        Initialize the feedback system with a SQLite database for storage.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_db()
        logger.info(f"Feedback system initialized with database at {db_path}")
    
    def _initialize_db(self) -> None:
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table for storing module feedback
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_name TEXT NOT NULL,
            model_used TEXT NOT NULL,
            feedback_type TEXT NOT NULL, 
            feedback_detail TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT
        )
        ''')
        
        # Table for storing optimization results
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS optimization_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_name TEXT NOT NULL,
            target_model TEXT NOT NULL,
            original_tokens INTEGER,
            optimized_tokens INTEGER,
            improvement_percent REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_applied BOOLEAN DEFAULT 0
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_feedback(
        self, 
        module_name: str, 
        model_used: str, 
        feedback_type: str, 
        feedback_detail: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> int:
        """
        Record feedback for a context module.
        
        Args:
            module_name: Name of the context module receiving feedback
            model_used: AI model that used the module (e.g., gpt-4, claude-3)
            feedback_type: Type of feedback (positive, negative, suggestion)
            feedback_detail: Optional detailed feedback
            session_id: Optional session identifier
        
        Returns:
            ID of the inserted feedback record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            INSERT INTO module_feedback 
            (module_name, model_used, feedback_type, feedback_detail, session_id) 
            VALUES (?, ?, ?, ?, ?)
            ''', 
            (module_name, model_used, feedback_type, feedback_detail, session_id)
        )
        
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Recorded {feedback_type} feedback for module {module_name}")
        return feedback_id
    
    def batch_add_feedback(self, feedback_data: List[Dict]) -> List[int]:
        """
        Add multiple feedback entries in a single transaction.
        
        Args:
            feedback_data: List of dictionaries containing feedback information
        
        Returns:
            List of inserted feedback IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        feedback_ids = []
        
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            for feedback in feedback_data:
                cursor.execute(
                    '''
                    INSERT INTO module_feedback 
                    (module_name, model_used, feedback_type, feedback_detail, session_id) 
                    VALUES (?, ?, ?, ?, ?)
                    ''', 
                    (
                        feedback.get("module_name"),
                        feedback.get("model_used"),
                        feedback.get("feedback_type"),
                        feedback.get("feedback_detail"),
                        feedback.get("session_id")
                    )
                )
                feedback_ids.append(cursor.lastrowid)
            
            cursor.execute("COMMIT")
        except Exception as e:
            cursor.execute("ROLLBACK")
            logger.error(f"Error adding batch feedback: {e}")
            raise e
        finally:
            conn.close()
        
        logger.info(f"Added {len(feedback_ids)} feedback entries")
        return feedback_ids
    
    def record_optimization(
        self,
        module_name: str,
        target_model: str,
        original_tokens: int,
        optimized_tokens: int,
        improvement_percent: float,
        is_applied: bool = False
    ) -> int:
        """
        Record the results of a module optimization.
        
        Args:
            module_name: Name of the optimized module
            target_model: AI model the optimization targets
            original_tokens: Token count of original module
            optimized_tokens: Token count of optimized module
            improvement_percent: Percentage improvement in evaluation
            is_applied: Whether the optimization was applied
        
        Returns:
            ID of the inserted optimization record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            INSERT INTO optimization_results 
            (module_name, target_model, original_tokens, optimized_tokens, 
            improvement_percent, is_applied) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', 
            (
                module_name, target_model, original_tokens, optimized_tokens, 
                improvement_percent, is_applied
            )
        )
        
        result_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Recorded optimization for {module_name} with {improvement_percent}% improvement")
        return result_id
    
    def mark_optimization_applied(self, module_name: str, target_model: str) -> bool:
        """
        Mark an optimization as applied in production.
        
        Args:
            module_name: Name of the module
            target_model: AI model the optimization targets
        
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            UPDATE optimization_results
            SET is_applied = 1
            WHERE module_name = ? AND target_model = ?
            ORDER BY timestamp DESC
            LIMIT 1
            ''',
            (module_name, target_model)
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Marked optimization for {module_name} as applied")
        else:
            logger.warning(f"No optimization found for {module_name}")
        
        return success
    
    def get_modules_needing_optimization(
        self, 
        threshold: float = 0.3, 
        min_feedback_count: int = 3,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get a list of modules that need optimization based on negative feedback.
        
        Args:
            threshold: Minimum ratio of negative feedback to trigger optimization
            min_feedback_count: Minimum number of feedback entries required
            limit: Maximum number of modules to return
        
        Returns:
            List of modules sorted by optimization priority
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
        WITH feedback_counts AS (
            SELECT 
                module_name,
                COUNT(*) as total_feedback,
                SUM(CASE WHEN feedback_type = 'negative' THEN 1 ELSE 0 END) as negative_count,
                SUM(CASE WHEN feedback_type = 'positive' THEN 1 ELSE 0 END) as positive_count
            FROM module_feedback
            GROUP BY module_name
            HAVING total_feedback >= ?
        )
        SELECT 
            module_name,
            total_feedback,
            negative_count,
            positive_count,
            CAST(negative_count AS REAL) / total_feedback as negative_ratio
        FROM feedback_counts
        WHERE negative_ratio >= ?
        ORDER BY negative_ratio DESC, total_feedback DESC
        LIMIT ?
        '''
        
        cursor.execute(query, (min_feedback_count, threshold, limit))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        logger.info(f"Found {len(results)} modules needing optimization")
        return results
    
    def get_module_performance(self, module_name: str) -> Dict:
        """
        Get performance metrics for a specific module.
        
        Args:
            module_name: Name of the module to analyze
        
        Returns:
            Dictionary with module performance metrics
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get feedback statistics
        cursor.execute(
            '''
            SELECT 
                COUNT(*) as total_feedback,
                SUM(CASE WHEN feedback_type = 'negative' THEN 1 ELSE 0 END) as negative_count,
                SUM(CASE WHEN feedback_type = 'positive' THEN 1 ELSE 0 END) as positive_count
            FROM module_feedback
            WHERE module_name = ?
            ''',
            (module_name,)
        )
        feedback_stats = dict(cursor.fetchone())
        
        # Get optimization history
        cursor.execute(
            '''
            SELECT 
                target_model,
                original_tokens,
                optimized_tokens,
                improvement_percent,
                is_applied,
                datetime(timestamp) as timestamp
            FROM optimization_results
            WHERE module_name = ?
            ORDER BY timestamp DESC
            ''',
            (module_name,)
        )
        optimization_history = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "module_name": module_name,
            "feedback_stats": feedback_stats,
            "optimization_history": optimization_history
        }
    
    def generate_performance_report(self, output_file: Optional[str] = None) -> Dict:
        """
        Generate a comprehensive performance report for all modules.
        
        Args:
            output_file: Optional path to save the report as JSON
        
        Returns:
            Dictionary containing the full performance report
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get overall statistics
        cursor.execute("SELECT COUNT(DISTINCT module_name) as total_modules FROM module_feedback")
        total_modules = cursor.fetchone()["total_modules"]
        
        cursor.execute("SELECT COUNT(*) as total_feedback FROM module_feedback")
        total_feedback = cursor.fetchone()["total_feedback"]
        
        cursor.execute("SELECT COUNT(*) as total_optimizations FROM optimization_results")
        total_optimizations = cursor.fetchone()["total_optimizations"]
        
        cursor.execute("SELECT AVG(improvement_percent) as avg_improvement FROM optimization_results")
        avg_improvement = cursor.fetchone()["avg_improvement"] or 0
        
        # Get top modules by negative feedback
        cursor.execute(
            '''
            SELECT 
                module_name,
                COUNT(*) as feedback_count,
                SUM(CASE WHEN feedback_type = 'negative' THEN 1 ELSE 0 END) as negative_count
            FROM module_feedback
            GROUP BY module_name
            ORDER BY negative_count DESC
            LIMIT 10
            '''
        )
        top_negative_feedback = [dict(row) for row in cursor.fetchall()]
        
        # Get top modules by positive feedback
        cursor.execute(
            '''
            SELECT 
                module_name,
                COUNT(*) as feedback_count,
                SUM(CASE WHEN feedback_type = 'positive' THEN 1 ELSE 0 END) as positive_count
            FROM module_feedback
            GROUP BY module_name
            ORDER BY positive_count DESC
            LIMIT 10
            '''
        )
        top_positive_feedback = [dict(row) for row in cursor.fetchall()]
        
        # Get recent optimizations
        cursor.execute(
            '''
            SELECT 
                module_name,
                target_model,
                improvement_percent,
                is_applied,
                datetime(timestamp) as timestamp
            FROM optimization_results
            ORDER BY timestamp DESC
            LIMIT 10
            '''
        )
        recent_optimizations = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_modules": total_modules,
                "total_feedback": total_feedback,
                "total_optimizations": total_optimizations,
                "average_improvement": round(avg_improvement, 2)
            },
            "top_negative_feedback": top_negative_feedback,
            "top_positive_feedback": top_positive_feedback,
            "recent_optimizations": recent_optimizations
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Performance report saved to {output_file}")
        
        return report

def main():
    """Command-line interface for the feedback system."""
    parser = argparse.ArgumentParser(description="Context Module Feedback System")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add feedback command
    add_parser = subparsers.add_parser("add", help="Add feedback for a module")
    add_parser.add_argument("module_name", help="Name of the context module")
    add_parser.add_argument("model", help="AI model that used the module")
    add_parser.add_argument("feedback_type", choices=["positive", "negative", "suggestion"],
                           help="Type of feedback")
    add_parser.add_argument("--detail", help="Detailed feedback")
    add_parser.add_argument("--session", help="Session identifier")
    
    # Batch add feedback command
    batch_parser = subparsers.add_parser("batch-add", help="Add multiple feedback entries from JSON")
    batch_parser.add_argument("input_file", help="JSON file containing feedback data")
    
    # Record optimization command
    optimize_parser = subparsers.add_parser("record-optimization", help="Record module optimization")
    optimize_parser.add_argument("module_name", help="Name of the optimized module")
    optimize_parser.add_argument("model", help="Target AI model")
    optimize_parser.add_argument("original_tokens", type=int, help="Original token count")
    optimize_parser.add_argument("optimized_tokens", type=int, help="Optimized token count")
    optimize_parser.add_argument("improvement", type=float, help="Improvement percentage")
    optimize_parser.add_argument("--applied", action="store_true", help="Mark as applied")
    
    # Mark as applied command
    apply_parser = subparsers.add_parser("mark-applied", help="Mark optimization as applied")
    apply_parser.add_argument("module_name", help="Name of the module")
    apply_parser.add_argument("model", help="Target AI model")
    
    # Modules needing optimization command
    needs_parser = subparsers.add_parser("show-needs-optimization", 
                               help="Show modules needing optimization")
    needs_parser.add_argument("--threshold", type=float, default=0.3,
                            help="Minimum negative feedback ratio")
    needs_parser.add_argument("--min-feedback", type=int, default=3,
                            help="Minimum feedback entries required")
    needs_parser.add_argument("--limit", type=int, default=10,
                            help="Maximum number of modules to return")
    needs_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    # Module performance command
    perf_parser = subparsers.add_parser("show-performance", help="Show module performance")
    perf_parser.add_argument("module_name", help="Name of the module")
    perf_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    # Generate report command
    report_parser = subparsers.add_parser("generate-report", help="Generate performance report")
    report_parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    # Initialize feedback system
    feedback_system = ContextFeedback()
    
    if args.command == "add":
        feedback_id = feedback_system.add_feedback(
            args.module_name, args.model, args.feedback_type, args.detail, args.session
        )
        print(f"Added feedback with ID: {feedback_id}")
    
    elif args.command == "batch-add":
        with open(args.input_file, 'r') as f:
            feedback_data = json.load(f)
        
        feedback_ids = feedback_system.batch_add_feedback(feedback_data)
        print(f"Added {len(feedback_ids)} feedback entries")
    
    elif args.command == "record-optimization":
        result_id = feedback_system.record_optimization(
            args.module_name, args.model,
            args.original_tokens, args.optimized_tokens,
            args.improvement, args.applied
        )
        print(f"Recorded optimization with ID: {result_id}")
    
    elif args.command == "mark-applied":
        success = feedback_system.mark_optimization_applied(args.module_name, args.model)
        if success:
            print(f"Marked optimization for {args.module_name} as applied")
        else:
            print(f"No optimization found for {args.module_name}")
            sys.exit(1)
    
    elif args.command == "show-needs-optimization":
        modules = feedback_system.get_modules_needing_optimization(
            args.threshold, args.min_feedback, args.limit
        )
        
        if args.json:
            print(json.dumps(modules, indent=2))
        else:
            print(f"Modules needing optimization (threshold: {args.threshold}, "
                 f"min feedback: {args.min_feedback}):")
            for i, module in enumerate(modules, 1):
                print(f"{i}. {module['module_name']}")
                print(f"   Negative ratio: {module['negative_ratio']:.2f} "
                     f"({module['negative_count']}/{module['total_feedback']})")
    
    elif args.command == "show-performance":
        performance = feedback_system.get_module_performance(args.module_name)
        
        if args.json:
            print(json.dumps(performance, indent=2))
        else:
            stats = performance["feedback_stats"]
            print(f"Performance for module: {args.module_name}")
            print(f"Total feedback: {stats['total_feedback']}")
            print(f"Positive feedback: {stats['positive_count']}")
            print(f"Negative feedback: {stats['negative_count']}")
            
            if performance["optimization_history"]:
                print("\nOptimization history:")
                for opt in performance["optimization_history"]:
                    applied = "✅ Applied" if opt["is_applied"] else "❌ Not applied"
                    print(f"- {opt['timestamp']}: {opt['improvement_percent']:.2f}% improvement "
                         f"({opt['target_model']}) {applied}")
    
    elif args.command == "generate-report":
        report = feedback_system.generate_performance_report(args.output)
        
        if not args.output:
            print(json.dumps(report, indent=2))
        else:
            print(f"Report generated and saved to {args.output}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 