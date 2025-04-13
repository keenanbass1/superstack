import os
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('context_feedback')

class ContextFeedback:
    """Manages feedback and optimization history for context modules"""
    
    def __init__(self, db_path=None):
        """
        Initialize with path to SQLite database
        
        Args:
            db_path: Path to SQLite database file. If None, uses default path
        """
        if db_path is None:
            # Use a default path in the project directory
            script_dir = Path(__file__).parent.resolve()
            db_path = script_dir / "context_optimization.db"
            
        self.db_path = Path(db_path)
        self._init_database()
        logger.info(f"Initialized context feedback system with database at {self.db_path}")
        
    def _init_database(self):
        """Initialize the database schema if it doesn't exist"""
        try:
            # Create database directory if it doesn't exist
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Connect to database and create tables if they don't exist
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create feedback table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                module_name TEXT NOT NULL,
                target_model TEXT NOT NULL,
                score INTEGER NOT NULL,
                comment TEXT,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            ''')
            
            # Create optimization_results table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_results (
                id TEXT PRIMARY KEY,
                module_name TEXT NOT NULL,
                target_model TEXT NOT NULL,
                original_score REAL,
                optimized_score REAL,
                improvement REAL,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                applied BOOLEAN NOT NULL DEFAULT 0,
                error TEXT
            )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
            
    def add_feedback(self, module_name, target_model, score, comment=None, source="user"):
        """
        Add feedback for a context module
        
        Args:
            module_name: Name of the module
            target_model: Target model used (e.g., claude, gpt)
            score: Score (1-10) indicating effectiveness
            comment: Optional comment about the module
            source: Source of feedback (user, automated, etc.)
            
        Returns:
            Dictionary with feedback details and success status
        """
        try:
            # Validate input
            if not module_name or not target_model:
                return {"success": False, "error": "Module name and target model are required"}
                
            if not isinstance(score, int) or score < 1 or score > 10:
                return {"success": False, "error": "Score must be an integer between 1 and 10"}
                
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate UUID for feedback
            feedback_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Insert feedback
            cursor.execute(
                """
                INSERT INTO feedback 
                (id, module_name, target_model, score, comment, source, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (feedback_id, module_name, target_model, score, comment, source, timestamp)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added feedback for module {module_name}: score {score}")
            
            return {
                "success": True,
                "id": feedback_id,
                "module_name": module_name,
                "target_model": target_model,
                "score": score,
                "comment": comment,
                "source": source,
                "timestamp": timestamp
            }
            
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
            return {"success": False, "error": str(e)}
            
    def add_optimization_result(self, module_name, target_model, evaluation_result, applied=False):
        """
        Add optimization result for a context module
        
        Args:
            module_name: Name of the module
            target_model: Target model used
            evaluation_result: Dictionary with evaluation results
            applied: Whether the optimization was applied (saved)
            
        Returns:
            Dictionary with result details and success status
        """
        try:
            # Validate input
            if not module_name or not target_model:
                return {"success": False, "error": "Module name and target model are required"}
                
            if not isinstance(evaluation_result, dict):
                return {"success": False, "error": "Evaluation result must be a dictionary"}
                
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate UUID for result
            result_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Determine status
            if evaluation_result.get("success", False):
                status = "success"
                error = None
            else:
                status = "failed"
                error = evaluation_result.get("error")
                
            # Extract scores and improvement
            original_score = evaluation_result.get("original_score")
            optimized_score = evaluation_result.get("optimized_score")
            improvement = evaluation_result.get("improvement")
            
            # Insert result
            cursor.execute(
                """
                INSERT INTO optimization_results 
                (id, module_name, target_model, original_score, optimized_score, 
                improvement, timestamp, status, applied, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (result_id, module_name, target_model, original_score, optimized_score, 
                improvement, timestamp, status, applied, error)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Added optimization result for module {module_name}: improvement {improvement}, applied: {applied}")
            
            return {
                "success": True,
                "id": result_id,
                "module_name": module_name,
                "target_model": target_model,
                "original_score": original_score,
                "optimized_score": optimized_score,
                "improvement": improvement,
                "timestamp": timestamp,
                "status": status,
                "applied": applied,
                "error": error
            }
            
        except Exception as e:
            logger.error(f"Error adding optimization result: {e}")
            return {"success": False, "error": str(e)}
            
    def get_module_feedback(self, module_name=None, target_model=None, limit=10):
        """
        Get feedback for a module or all modules
        
        Args:
            module_name: Optional module name filter
            target_model: Optional target model filter
            limit: Maximum number of results to return
            
        Returns:
            List of feedback entries
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query
            query = "SELECT * FROM feedback"
            params = []
            
            if module_name or target_model:
                query += " WHERE"
                
                if module_name:
                    query += " module_name = ?"
                    params.append(module_name)
                    
                    if target_model:
                        query += " AND target_model = ?"
                        params.append(target_model)
                elif target_model:
                    query += " target_model = ?"
                    params.append(target_model)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            # Execute query
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                result = dict(zip(column_names, row))
                results.append(result)
                
            conn.close()
            
            return {"success": True, "feedback": results}
            
        except Exception as e:
            logger.error(f"Error getting module feedback: {e}")
            return {"success": False, "error": str(e)}
            
    def get_optimization_results(self, module_name=None, target_model=None, limit=10):
        """
        Get optimization results for a module or all modules
        
        Args:
            module_name: Optional module name filter
            target_model: Optional target model filter
            limit: Maximum number of results to return
            
        Returns:
            List of optimization result entries
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query
            query = "SELECT * FROM optimization_results"
            params = []
            
            if module_name or target_model:
                query += " WHERE"
                
                if module_name:
                    query += " module_name = ?"
                    params.append(module_name)
                    
                    if target_model:
                        query += " AND target_model = ?"
                        params.append(target_model)
                elif target_model:
                    query += " target_model = ?"
                    params.append(target_model)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            # Execute query
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                result = dict(zip(column_names, row))
                results.append(result)
                
            conn.close()
            
            return {"success": True, "results": results}
            
        except Exception as e:
            logger.error(f"Error getting optimization results: {e}")
            return {"success": False, "error": str(e)}
            
    def calculate_module_effectiveness(self, module_name, target_model=None):
        """
        Calculate effectiveness of a module based on feedback
        
        Args:
            module_name: Module name
            target_model: Optional target model filter
            
        Returns:
            Dictionary with effectiveness metrics
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            
            # Query to get feedback
            query = "SELECT * FROM feedback WHERE module_name = ?"
            params = [module_name]
            
            if target_model:
                query += " AND target_model = ?"
                params.append(target_model)
                
            # Load into dataframe
            df = pd.read_sql_query(query, conn, params=params)
            
            if df.empty:
                return {
                    "success": True,
                    "module_name": module_name,
                    "target_model": target_model,
                    "feedback_count": 0,
                    "avg_score": None,
                    "effectiveness": None,
                    "needs_optimization": False
                }
            
            # Calculate metrics
            feedback_count = len(df)
            avg_score = df['score'].mean()
            
            # Effectiveness is normalized to 0-100%
            effectiveness = (avg_score - 1) / 9 * 100
            
            # Get latest optimization if any
            query = "SELECT * FROM optimization_results WHERE module_name = ?"
            params = [module_name]
            
            if target_model:
                query += " AND target_model = ?"
                params.append(target_model)
                
            query += " ORDER BY timestamp DESC LIMIT 1"
            
            # Load latest optimization
            opt_df = pd.read_sql_query(query, conn, params=params)
            
            # Determine if optimization is needed
            needs_optimization = False
            last_optimization = None
            
            if opt_df.empty:
                # No previous optimization, needs it if effectiveness is low
                needs_optimization = effectiveness < 70 and feedback_count >= 3
            else:
                # Get latest optimization data
                last_optimization = opt_df.iloc[0].to_dict()
                last_timestamp = datetime.fromisoformat(last_optimization['timestamp'])
                
                # Need optimization if:
                # 1. Last optimization was over 30 days ago AND
                # 2. Effectiveness is less than 70% AND
                # 3. We have at least 3 pieces of feedback
                needs_optimization = (
                    (datetime.now() - last_timestamp).days > 30 and
                    effectiveness < 70 and
                    feedback_count >= 3
                )
            
            conn.close()
            
            return {
                "success": True,
                "module_name": module_name,
                "target_model": target_model,
                "feedback_count": feedback_count,
                "avg_score": round(avg_score, 2) if avg_score is not None else None,
                "effectiveness": round(effectiveness, 2) if effectiveness is not None else None,
                "needs_optimization": needs_optimization,
                "last_optimization": last_optimization
            }
            
        except Exception as e:
            logger.error(f"Error calculating module effectiveness: {e}")
            return {"success": False, "error": str(e)}
            
    def identify_modules_for_improvement(self, min_feedback=3, max_effectiveness=70, target_model=None):
        """
        Identify modules that need optimization based on feedback
        
        Args:
            min_feedback: Minimum number of feedback entries required
            max_effectiveness: Maximum effectiveness threshold
            target_model: Optional target model filter
            
        Returns:
            List of modules that need optimization
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            
            # First, get all modules with enough feedback
            query = """
            SELECT module_name, COUNT(*) as feedback_count, AVG(score) as avg_score
            FROM feedback
            """
            
            params = []
            if target_model:
                query += " WHERE target_model = ?"
                params.append(target_model)
                
            query += " GROUP BY module_name HAVING COUNT(*) >= ?"
            params.append(min_feedback)
            
            # Load into dataframe
            df = pd.read_sql_query(query, conn, params=params)
            
            if df.empty:
                return {
                    "success": True,
                    "modules_to_improve": [],
                    "target_model": target_model
                }
            
            # Calculate effectiveness for each module
            df['effectiveness'] = (df['avg_score'] - 1) / 9 * 100
            
            # Filter by effectiveness threshold
            low_effectiveness = df[df['effectiveness'] <= max_effectiveness]
            
            # Get list of modules that haven't been optimized recently
            modules_to_improve = []
            
            for _, row in low_effectiveness.iterrows():
                module_name = row['module_name']
                
                # Check if module was optimized recently
                query = """
                SELECT *
                FROM optimization_results
                WHERE module_name = ?
                """
                
                opt_params = [module_name]
                if target_model:
                    query += " AND target_model = ?"
                    opt_params.append(target_model)
                    
                query += " ORDER BY timestamp DESC LIMIT 1"
                
                opt_df = pd.read_sql_query(query, conn, params=opt_params)
                
                if opt_df.empty:
                    # No previous optimization, add to list
                    modules_to_improve.append({
                        "module_name": module_name,
                        "feedback_count": int(row['feedback_count']),
                        "avg_score": round(float(row['avg_score']), 2),
                        "effectiveness": round(float(row['effectiveness']), 2),
                        "last_optimization": None
                    })
                else:
                    # Check if last optimization was more than 30 days ago
                    last_opt = opt_df.iloc[0]
                    last_timestamp = datetime.fromisoformat(last_opt['timestamp'])
                    
                    if (datetime.now() - last_timestamp).days > 30:
                        modules_to_improve.append({
                            "module_name": module_name,
                            "feedback_count": int(row['feedback_count']),
                            "avg_score": round(float(row['avg_score']), 2),
                            "effectiveness": round(float(row['effectiveness']), 2),
                            "last_optimization": last_timestamp.isoformat(),
                            "last_improvement": float(last_opt['improvement']) if last_opt['improvement'] else None
                        })
            
            conn.close()
            
            # Sort by effectiveness (ascending)
            modules_to_improve.sort(key=lambda x: x["effectiveness"])
            
            return {
                "success": True,
                "modules_to_improve": modules_to_improve,
                "target_model": target_model
            }
            
        except Exception as e:
            logger.error(f"Error identifying modules for improvement: {e}")
            return {"success": False, "error": str(e)}
            
    def calculate_optimization_success_rate(self, target_model=None, min_improvement=1):
        """
        Calculate success rate of optimizations
        
        Args:
            target_model: Optional target model filter
            min_improvement: Minimum improvement for optimization to be considered successful
            
        Returns:
            Dictionary with success metrics
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            
            # Build query for successful optimizations
            query = """
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful,
                   SUM(CASE WHEN status = 'success' AND improvement >= ? THEN 1 ELSE 0 END) as improved,
                   AVG(CASE WHEN status = 'success' THEN improvement ELSE NULL END) as avg_improvement
            FROM optimization_results
            """
            
            params = [min_improvement]
            if target_model:
                query += " WHERE target_model = ?"
                params.append(target_model)
            
            # Execute query
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            # Parse results
            total = row[0]
            successful = row[1]
            improved = row[2]
            avg_improvement = row[3]
            
            # Calculate rates
            success_rate = (successful / total * 100) if total > 0 else 0
            improvement_rate = (improved / successful * 100) if successful > 0 else 0
            
            conn.close()
            
            return {
                "success": True,
                "total_optimizations": total,
                "successful_optimizations": successful,
                "improved_optimizations": improved,
                "success_rate": round(success_rate, 2),
                "improvement_rate": round(improvement_rate, 2),
                "avg_improvement": round(avg_improvement, 2) if avg_improvement else 0,
                "target_model": target_model
            }
            
        except Exception as e:
            logger.error(f"Error calculating optimization success rate: {e}")
            return {"success": False, "error": str(e)}
            
    def export_data(self, output_path=None):
        """
        Export feedback and optimization data to JSON file
        
        Args:
            output_path: Optional path for output file
            
        Returns:
            Dictionary with export details
        """
        try:
            # Determine output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"context_data_export_{timestamp}.json"
                
            output_path = Path(output_path)
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            
            # Get all feedback
            feedback_df = pd.read_sql_query("SELECT * FROM feedback ORDER BY timestamp DESC", conn)
            feedback_records = feedback_df.to_dict('records')
            
            # Get all optimization results
            opt_df = pd.read_sql_query("SELECT * FROM optimization_results ORDER BY timestamp DESC", conn)
            opt_records = opt_df.to_dict('records')
            
            # Calculate summary statistics
            total_feedback = len(feedback_records)
            total_optimizations = len(opt_records)
            avg_improvement = opt_df['improvement'].mean() if not opt_df.empty else 0
            
            # Create export data
            export_data = {
                "export_date": datetime.now().isoformat(),
                "summary": {
                    "total_feedback": total_feedback,
                    "total_optimizations": total_optimizations,
                    "avg_improvement": round(avg_improvement, 2) if avg_improvement is not None else 0
                },
                "feedback": feedback_records,
                "optimization_results": opt_records
            }
            
            # Write to file
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            conn.close()
            
            logger.info(f"Exported data to {output_path}")
            
            return {
                "success": True,
                "output_path": str(output_path),
                "total_feedback": total_feedback,
                "total_optimizations": total_optimizations
            }
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Command-line interface
    import argparse
    
    parser = argparse.ArgumentParser(description="Context module feedback system")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add feedback command
    add_parser = subparsers.add_parser("add", help="Add feedback for a module")
    add_parser.add_argument("module", help="Module name")
    add_parser.add_argument("score", type=int, help="Score (1-10)")
    add_parser.add_argument("--model", "-m", default="claude", help="Target model")
    add_parser.add_argument("--comment", "-c", help="Optional comment")
    add_parser.add_argument("--source", "-s", default="user", help="Source of feedback")
    
    # Get feedback command
    get_parser = subparsers.add_parser("get", help="Get feedback for modules")
    get_parser.add_argument("--module", "-m", help="Optional module name filter")
    get_parser.add_argument("--model", "-t", help="Optional target model filter")
    get_parser.add_argument("--limit", "-l", type=int, default=10, help="Maximum results")
    
    # List modules for improvement command
    improve_parser = subparsers.add_parser("improve", help="List modules needing improvement")
    improve_parser.add_argument("--model", "-m", help="Target model")
    improve_parser.add_argument("--min-feedback", type=int, default=3, help="Minimum feedback count")
    improve_parser.add_argument("--max-effectiveness", type=float, default=70, help="Max effectiveness threshold")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export feedback data")
    export_parser.add_argument("--output", "-o", help="Output file path")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show optimization statistics")
    stats_parser.add_argument("--model", "-m", help="Target model filter")
    
    args = parser.parse_args()
    
    # Initialize feedback system
    feedback_system = ContextFeedback()
    
    if args.command == "add":
        # Add feedback
        result = feedback_system.add_feedback(
            args.module, 
            args.model, 
            args.score, 
            args.comment, 
            args.source
        )
        
        if result["success"]:
            print(f"Added feedback for module {args.module}")
            print(f"ID: {result['id']}")
            print(f"Score: {result['score']}")
        else:
            print(f"Error: {result['error']}")
            
    elif args.command == "get":
        # Get feedback
        result = feedback_system.get_module_feedback(args.module, args.model, args.limit)
        
        if result["success"]:
            feedback = result["feedback"]
            print(f"Found {len(feedback)} feedback entries")
            
            if feedback:
                print("\nLatest feedback:")
                for item in feedback[:5]:  # Show first 5
                    print(f"  {item['module_name']} - Score: {item['score']} - {item['timestamp']}")
                    if item['comment']:
                        print(f"    Comment: {item['comment']}")
        else:
            print(f"Error: {result['error']}")
            
    elif args.command == "improve":
        # List modules for improvement
        result = feedback_system.identify_modules_for_improvement(
            args.min_feedback,
            args.max_effectiveness,
            args.model
        )
        
        if result["success"]:
            modules = result["modules_to_improve"]
            print(f"Found {len(modules)} modules needing improvement")
            
            if modules:
                print("\nModules to improve:")
                for i, module in enumerate(modules, 1):
                    print(f"{i}. {module['module_name']}")
                    print(f"   Effectiveness: {module['effectiveness']}% (avg score: {module['avg_score']})")
                    print(f"   Feedback count: {module['feedback_count']}")
                    
                    if module.get('last_optimization'):
                        print(f"   Last optimized: {module['last_optimization']}")
                        if module.get('last_improvement'):
                            print(f"   Previous improvement: {module['last_improvement']}%")
        else:
            print(f"Error: {result['error']}")
            
    elif args.command == "export":
        # Export data
        result = feedback_system.export_data(args.output)
        
        if result["success"]:
            print(f"Exported {result['total_feedback']} feedback items and {result['total_optimizations']} optimization results")
            print(f"Output saved to: {result['output_path']}")
        else:
            print(f"Error: {result['error']}")
            
    elif args.command == "stats":
        # Show statistics
        result = feedback_system.calculate_optimization_success_rate(args.model)
        
        if result["success"]:
            print(f"\nOptimization Statistics:")
            print(f"Total optimizations: {result['total_optimizations']}")
            print(f"Success rate: {result['success_rate']}%")
            print(f"Improvement rate: {result['improvement_rate']}%")
            print(f"Average improvement: {result['avg_improvement']}%")
        else:
            print(f"Error: {result['error']}")
    else:
        parser.print_help() 