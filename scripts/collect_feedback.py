#!/usr/bin/env python3
"""
Context Module Feedback Collector

This script provides utilities for collecting, storing, and analyzing
user feedback on context modules to identify candidates for optimization.
"""

import os
import sys
import json
import yaml
import sqlite3
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging for the feedback collection process.
    
    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to a log file
        
    Returns:
        Configured logger
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    level = getattr(logging, log_level)
    
    handlers = []
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
    
    return logging.getLogger(__name__)

def load_config(config_path: str = "config/dsp_config.yaml") -> Dict[str, Any]:
    """
    Load the configuration from the specified path.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration as a dictionary
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def init_database(db_path: str) -> sqlite3.Connection:
    """
    Initialize the SQLite database for storing feedback.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Database connection
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create feedback table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS module_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_name TEXT NOT NULL,
        target_model TEXT,
        feedback_type TEXT NOT NULL,
        score INTEGER,
        comments TEXT,
        user_id TEXT,
        timestamp TEXT NOT NULL
    )
    ''')
    
    # Create optimization results table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS optimization_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_name TEXT NOT NULL,
        target_model TEXT,
        original_score REAL,
        optimized_score REAL,
        improvement REAL,
        timestamp TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    return conn

def record_feedback(
    db_conn: sqlite3.Connection,
    module_name: str,
    feedback_type: str,
    score: Optional[int] = None,
    comments: Optional[str] = None,
    target_model: Optional[str] = None,
    user_id: Optional[str] = None
) -> bool:
    """
    Record user feedback for a context module.
    
    Args:
        db_conn: Database connection
        module_name: Name of the context module
        feedback_type: Type of feedback (e.g., "effectiveness", "clarity", "relevance")
        score: Optional numeric rating (e.g., 1-5)
        comments: Optional text comments
        target_model: Optional target model identifier
        user_id: Optional user identifier
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cursor = db_conn.cursor()
        timestamp = datetime.now().isoformat()
        
        cursor.execute(
            '''
            INSERT INTO module_feedback 
            (module_name, target_model, feedback_type, score, comments, user_id, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (module_name, target_model, feedback_type, score, comments, user_id, timestamp)
        )
        
        db_conn.commit()
        return True
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when recording feedback: {str(e)}")
        return False

def record_optimization_result(
    db_conn: sqlite3.Connection,
    module_name: str,
    original_score: float,
    optimized_score: float,
    improvement: float,
    target_model: Optional[str] = None
) -> bool:
    """
    Record optimization results for a module.
    
    Args:
        db_conn: Database connection
        module_name: Name of the context module
        original_score: Score of the original module
        optimized_score: Score of the optimized module
        improvement: Percentage improvement
        target_model: Optional target model identifier
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cursor = db_conn.cursor()
        timestamp = datetime.now().isoformat()
        
        cursor.execute(
            '''
            INSERT INTO optimization_results 
            (module_name, target_model, original_score, optimized_score, improvement, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (module_name, target_model, original_score, optimized_score, improvement, timestamp)
        )
        
        db_conn.commit()
        return True
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when recording optimization result: {str(e)}")
        return False

def get_module_feedback(
    db_conn: sqlite3.Connection,
    module_name: Optional[str] = None,
    target_model: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get feedback for a specific module or all modules.
    
    Args:
        db_conn: Database connection
        module_name: Optional name of the module to filter by
        target_model: Optional target model to filter by
        limit: Maximum number of records to return
        
    Returns:
        List of feedback records
    """
    try:
        cursor = db_conn.cursor()
        
        query = "SELECT * FROM module_feedback"
        params = []
        
        if module_name or target_model:
            query += " WHERE"
            
            if module_name:
                query += " module_name = ?"
                params.append(module_name)
                
                if target_model:
                    query += " AND"
            
            if target_model:
                query += " target_model = ?"
                params.append(target_model)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        
        return result
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when retrieving feedback: {str(e)}")
        return []

def get_optimization_results(
    db_conn: sqlite3.Connection,
    module_name: Optional[str] = None,
    target_model: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get optimization results for a specific module or all modules.
    
    Args:
        db_conn: Database connection
        module_name: Optional name of the module to filter by
        target_model: Optional target model to filter by
        limit: Maximum number of records to return
        
    Returns:
        List of optimization result records
    """
    try:
        cursor = db_conn.cursor()
        
        query = "SELECT * FROM optimization_results"
        params = []
        
        if module_name or target_model:
            query += " WHERE"
            
            if module_name:
                query += " module_name = ?"
                params.append(module_name)
                
                if target_model:
                    query += " AND"
            
            if target_model:
                query += " target_model = ?"
                params.append(target_model)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        
        return result
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when retrieving optimization results: {str(e)}")
        return []

def calculate_module_effectiveness(
    db_conn: sqlite3.Connection,
    module_name: str,
    target_model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate the effectiveness score of a module based on feedback.
    
    Args:
        db_conn: Database connection
        module_name: Name of the module
        target_model: Optional target model to filter by
        
    Returns:
        Dictionary with effectiveness metrics
    """
    try:
        cursor = db_conn.cursor()
        
        params = [module_name]
        model_filter = ""
        
        if target_model:
            model_filter = "AND target_model = ?"
            params.append(target_model)
        
        # Get all feedback for the module
        cursor.execute(
            f'''
            SELECT feedback_type, score, timestamp
            FROM module_feedback
            WHERE module_name = ? {model_filter}
            ORDER BY timestamp DESC
            ''',
            params
        )
        
        feedback_data = cursor.fetchall()
        
        if not feedback_data:
            return {
                "module_name": module_name,
                "feedback_count": 0,
                "average_score": None,
                "recent_score": None,
                "needs_improvement": False
            }
        
        # Calculate metrics
        feedback_count = len(feedback_data)
        scores = [row[1] for row in feedback_data if row[1] is not None]
        
        average_score = sum(scores) / len(scores) if scores else None
        recent_score = scores[0] if scores else None
        
        # Determine if module needs improvement (score < 3.5 or high volume of low scores)
        low_scores = [s for s in scores if s is not None and s < 3]
        low_score_ratio = len(low_scores) / len(scores) if scores else 0
        
        needs_improvement = (average_score is not None and average_score < 3.5) or low_score_ratio > 0.3
        
        return {
            "module_name": module_name,
            "feedback_count": feedback_count,
            "average_score": average_score,
            "recent_score": recent_score,
            "low_score_ratio": low_score_ratio,
            "needs_improvement": needs_improvement
        }
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when calculating effectiveness: {str(e)}")
        return {
            "module_name": module_name,
            "error": str(e),
            "feedback_count": 0,
            "needs_improvement": False
        }

def identify_modules_for_improvement(
    db_conn: sqlite3.Connection,
    threshold_score: float = 3.5,
    threshold_feedback_count: int = 5,
    target_model: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Identify modules that need improvement based on feedback.
    
    Args:
        db_conn: Database connection
        threshold_score: Score threshold below which a module is flagged
        threshold_feedback_count: Minimum feedback count to consider
        target_model: Optional target model to filter by
        
    Returns:
        List of modules that need improvement, with metrics
    """
    try:
        cursor = db_conn.cursor()
        
        # Get all unique module names
        model_filter = ""
        params = []
        
        if target_model:
            model_filter = "WHERE target_model = ?"
            params.append(target_model)
        
        cursor.execute(
            f'''
            SELECT DISTINCT module_name
            FROM module_feedback
            {model_filter}
            ''',
            params
        )
        
        module_names = [row[0] for row in cursor.fetchall()]
        
        # Calculate effectiveness for each module
        modules_to_improve = []
        
        for module_name in module_names:
            effectiveness = calculate_module_effectiveness(db_conn, module_name, target_model)
            
            if (effectiveness["feedback_count"] >= threshold_feedback_count and
                    (effectiveness.get("average_score") is not None and 
                     effectiveness["average_score"] < threshold_score)):
                modules_to_improve.append(effectiveness)
        
        # Sort by average score, lowest first
        return sorted(modules_to_improve, key=lambda x: x.get("average_score", float('inf')))
        
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when identifying modules for improvement: {str(e)}")
        return []

def calculate_optimization_success_rate(
    db_conn: sqlite3.Connection,
    target_model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate the success rate of optimization attempts.
    
    Args:
        db_conn: Database connection
        target_model: Optional target model to filter by
        
    Returns:
        Dictionary with success rate metrics
    """
    try:
        cursor = db_conn.cursor()
        
        model_filter = ""
        params = []
        
        if target_model:
            model_filter = "WHERE target_model = ?"
            params.append(target_model)
        
        cursor.execute(
            f'''
            SELECT improvement
            FROM optimization_results
            {model_filter}
            ''',
            params
        )
        
        results = cursor.fetchall()
        
        if not results:
            return {
                "total_optimizations": 0,
                "successful_optimizations": 0,
                "success_rate": 0,
                "average_improvement": None
            }
        
        total_optimizations = len(results)
        
        # Count optimizations with positive improvement
        improvements = [row[0] for row in results if row[0] is not None]
        successful_optimizations = sum(1 for imp in improvements if imp > 0)
        
        success_rate = successful_optimizations / total_optimizations if total_optimizations > 0 else 0
        average_improvement = sum(improvements) / len(improvements) if improvements else None
        
        return {
            "total_optimizations": total_optimizations,
            "successful_optimizations": successful_optimizations,
            "success_rate": success_rate,
            "average_improvement": average_improvement
        }
    except sqlite3.Error as e:
        logging.getLogger(__name__).error(f"Database error when calculating success rate: {str(e)}")
        return {
            "error": str(e),
            "total_optimizations": 0,
            "successful_optimizations": 0,
            "success_rate": 0,
            "average_improvement": None
        }

def export_data(
    db_conn: sqlite3.Connection,
    output_file: str,
    target_model: Optional[str] = None
) -> bool:
    """
    Export feedback and optimization data to a JSON file.
    
    Args:
        db_conn: Database connection
        output_file: Path to the output JSON file
        target_model: Optional target model to filter by
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get feedback and optimization data
        feedback_records = get_module_feedback(db_conn, target_model=target_model, limit=10000)
        optimization_results = get_optimization_results(db_conn, target_model=target_model, limit=10000)
        
        # Calculate summary metrics
        success_rate = calculate_optimization_success_rate(db_conn, target_model)
        modules_to_improve = identify_modules_for_improvement(db_conn, target_model=target_model)
        
        # Prepare export data
        export_data = {
            "feedback_records": feedback_records,
            "optimization_results": optimization_results,
            "summary": {
                "total_feedback": len(feedback_records),
                "total_optimizations": len(optimization_results),
                "optimization_success_rate": success_rate,
                "modules_needing_improvement": [m["module_name"] for m in modules_to_improve],
                "export_timestamp": datetime.now().isoformat()
            }
        }
        
        # Write to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Error exporting data: {str(e)}")
        return False

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Collect and manage context module feedback")
    
    parser.add_argument("--config", type=str, default="config/dsp_config.yaml",
                       help="Path to the configuration file")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add feedback command
    add_parser = subparsers.add_parser("add", help="Add new feedback")
    add_parser.add_argument("--module", type=str, required=True,
                           help="Name of the module")
    add_parser.add_argument("--type", type=str, required=True,
                           choices=["effectiveness", "clarity", "relevance", "completeness", "other"],
                           help="Type of feedback")
    add_parser.add_argument("--score", type=int, choices=range(1, 6),
                           help="Score (1-5)")
    add_parser.add_argument("--comment", type=str,
                           help="Feedback comment")
    add_parser.add_argument("--model", type=str,
                           help="Target model")
    add_parser.add_argument("--user", type=str,
                           help="User identifier")
    
    # Record optimization result command
    optimize_parser = subparsers.add_parser("optimize", help="Record optimization result")
    optimize_parser.add_argument("--module", type=str, required=True,
                               help="Name of the module")
    optimize_parser.add_argument("--original-score", type=float, required=True,
                               help="Score of the original module")
    optimize_parser.add_argument("--optimized-score", type=float, required=True,
                               help="Score of the optimized module")
    optimize_parser.add_argument("--improvement", type=float, 
                               help="Percentage improvement (calculated if not provided)")
    optimize_parser.add_argument("--model", type=str,
                               help="Target model")
    
    # List feedback command
    list_parser = subparsers.add_parser("list", help="List feedback")
    list_parser.add_argument("--module", type=str,
                           help="Filter by module name")
    list_parser.add_argument("--model", type=str,
                           help="Filter by target model")
    list_parser.add_argument("--limit", type=int, default=10,
                           help="Maximum number of records to return")
    
    # Identify modules for improvement command
    identify_parser = subparsers.add_parser("identify", help="Identify modules for improvement")
    identify_parser.add_argument("--threshold-score", type=float, default=3.5,
                               help="Score threshold for identifying modules")
    identify_parser.add_argument("--threshold-count", type=int, default=5,
                               help="Minimum feedback count threshold")
    identify_parser.add_argument("--model", type=str,
                               help="Filter by target model")
    identify_parser.add_argument("--output", type=str,
                               help="Path to save results as JSON")
    
    # Export data command
    export_parser = subparsers.add_parser("export", help="Export feedback and optimization data")
    export_parser.add_argument("--output", type=str, required=True,
                             help="Path to save export file")
    export_parser.add_argument("--model", type=str,
                             help="Filter by target model")
    
    # Common arguments
    parser.add_argument("--db", type=str,
                       help="Path to the SQLite database file (defaults to config path)")
    parser.add_argument("--log-level", type=str, default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                       help="Logging level")
    parser.add_argument("--log-file", type=str,
                       help="Path to log file")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Set up logging
    logger = setup_logging(args.log_level, args.log_file)
    
    # Load configuration
    config = load_config(args.config)
    
    # Determine database path
    db_path = args.db
    if not db_path:
        db_path = config.get('feedback', {}).get('database_path', 'data/feedback.db')
    
    # Initialize database
    db_conn = init_database(db_path)
    
    # Execute command
    if args.command == "add":
        success = record_feedback(
            db_conn=db_conn,
            module_name=args.module,
            feedback_type=args.type,
            score=args.score,
            comments=args.comment,
            target_model=args.model,
            user_id=args.user
        )
        
        if success:
            print(f"Successfully recorded feedback for module '{args.module}'")
        else:
            print("Failed to record feedback")
    
    elif args.command == "optimize":
        # Calculate improvement if not provided
        improvement = args.improvement
        if improvement is None and args.original_score > 0:
            improvement = ((args.optimized_score - args.original_score) / args.original_score) * 100
        
        success = record_optimization_result(
            db_conn=db_conn,
            module_name=args.module,
            original_score=args.original_score,
            optimized_score=args.optimized_score,
            improvement=improvement,
            target_model=args.model
        )
        
        if success:
            print(f"Successfully recorded optimization result for module '{args.module}'")
            print(f"Improvement: {improvement:.2f}%")
        else:
            print("Failed to record optimization result")
    
    elif args.command == "list":
        feedback_records = get_module_feedback(
            db_conn=db_conn,
            module_name=args.module,
            target_model=args.model,
            limit=args.limit
        )
        
        if feedback_records:
            print(f"Found {len(feedback_records)} feedback records:")
            for record in feedback_records:
                print(f"- Module: {record['module_name']}")
                print(f"  Type: {record['feedback_type']}")
                print(f"  Score: {record['score']}")
                print(f"  Date: {record['timestamp']}")
                if record['comments']:
                    print(f"  Comments: {record['comments']}")
                print()
        else:
            print("No feedback records found matching the criteria")
    
    elif args.command == "identify":
        modules = identify_modules_for_improvement(
            db_conn=db_conn,
            threshold_score=args.threshold_score,
            threshold_feedback_count=args.threshold_count,
            target_model=args.model
        )
        
        if modules:
            print(f"Found {len(modules)} modules needing improvement:")
            for module in modules:
                print(f"- Module: {module['module_name']}")
                print(f"  Average Score: {module['average_score']:.2f}")
                print(f"  Feedback Count: {module['feedback_count']}")
                print()
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump({"modules_for_improvement": modules}, f, indent=2)
                print(f"Results saved to {args.output}")
        else:
            print("No modules found that need improvement")
    
    elif args.command == "export":
        success = export_data(
            db_conn=db_conn,
            output_file=args.output,
            target_model=args.model
        )
        
        if success:
            print(f"Successfully exported data to {args.output}")
        else:
            print("Failed to export data")
    
    else:
        logger.error("No command specified")
        print("Please specify a command. Use --help for more information.")
    
    # Close database connection
    db_conn.close() 