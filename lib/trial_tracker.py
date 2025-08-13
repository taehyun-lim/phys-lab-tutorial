import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import re

class TrialTracker:
    def __init__(self):
        self.session_key = "trial_tracker_data"
        self.password_file = "data/password.json"
        self.sections = [
            "intro", "precision_accuracy", "uncertainty_range", 
            "one_measurement", "range_method", "std_dev_gaussian", "standard_form"
        ]
        
        # Question sequences within each section
        self.question_sequences = {
            "intro": ["intro_q3"],  # Intro section has one question
            "precision_accuracy": ["pa_q1", "pa_q2", "pa_q3", "pa_q4", "pa_q5", "pa_q6", "pa_q7", "pa_q8"],
            "uncertainty_range": ["uncertainty_q1", "uncertainty_q2", "uncertainty_q3", "uncertainty_q4"],
            "one_measurement": ["om_q1", "om_q2"],
            "range_method": ["range_q1", "range_q2"],
            "std_dev_gaussian": ["sd_q1", "sd_q2", "sd_q3", "sd_q4", "sd_q5"],
            "standard_form": ["sf_q1", "sf_q2", "sf_q3", "sf_q4"] # Corrected back to 4 questions
        }
        
        # Don't initialize here - wait until first use
    
    def _ensure_session_state(self):
        """Ensure session state is initialized - call this before any access"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                "trials": {},
                "start_time": datetime.now().isoformat(),
                "student_id": None,
                "email": None,
                "optional_responses": {},
                "session_complete": False,
                "completed_sections": set(),
                "completed_questions": {},
                "current_section": None,
                "current_question": None
            }
    
    def _safe_get(self, key, default=None):
        """Safely get a value from session state with error handling"""
        try:
            self._ensure_session_state()
            return st.session_state[self.session_key].get(key, default)
        except Exception as e:
            print(f"Warning: Error accessing session state key '{key}': {e}")
            return default
    
    def _safe_set(self, key, value):
        """Safely set a value in session state with error handling"""
        try:
            self._ensure_session_state()
            st.session_state[self.session_key][key] = value
        except Exception as e:
            print(f"Warning: Error setting session state key '{key}': {e}")
    
    def _load_password_config(self):
        """Load password configuration from JSON file"""
        try:
            if os.path.exists(self.password_file):
                with open(self.password_file, 'r') as f:
                    return json.load(f)
            return {"csv_download_password": "password", "admin_emails": []}
        except Exception as e:
            print(f"Warning: Error loading password config: {e}")
            return {"csv_download_password": "password", "admin_emails": []}
    
    def validate_email(self, email):
        """Validate that email ends with @hamilton.edu"""
        if not email or not isinstance(email, str):
            return False
        return email.strip().lower().endswith("@hamilton.edu")
    
    def initialize_session_state(self):
        """Initialize the session state for tracking trials"""
        self._ensure_session_state()
    
    def set_student_email(self, email):
        """Set the student's email address after validation"""
        if self.validate_email(email):
            self._safe_set("email", email.strip())
            return True
        return False
    
    def get_student_email(self):
        """Get the student's email address"""
        return self._safe_get("email", "Not provided")
    
    def get_student_id(self):
        """Get or create a student ID for this session"""
        student_id = self._safe_get("student_id")
        if student_id is None:
            # Generate a simple ID based on timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            student_id = f"student_{timestamp}"
            self._safe_set("student_id", student_id)
        return student_id
    
    def mark_section_complete(self, section_name):
        """Mark a section as complete"""
        try:
            self._ensure_session_state()
            completed_sections = self._safe_get("completed_sections", set())
            completed_sections.add(section_name)
            self._safe_set("completed_sections", completed_sections)
        except Exception as e:
            print(f"Warning: Error marking section complete: {e}")

    def mark_question_complete(self, section_name, question_id):
        """Mark a question as complete"""
        try:
            self._ensure_session_state()
            completed_questions = self._safe_get("completed_questions", {})
            if section_name not in completed_questions:
                completed_questions[section_name] = []
            if question_id not in completed_questions[section_name]:
                completed_questions[section_name].append(question_id)
            self._safe_set("completed_questions", completed_questions)
        except Exception as e:
            print(f"Warning: Error marking question complete: {e}")

    def is_section_final_question_completed(self, section_name):
        """Check if the final question of a section is completed"""
        try:
            question_sequence = self.question_sequences.get(section_name, [])
            if not question_sequence:
                return True  # No questions means section is always accessible
            
            final_question = question_sequence[-1]
            completed_questions = self._safe_get("completed_questions", {})
            section_questions = completed_questions.get(section_name, [])
            return final_question in section_questions
        except Exception as e:
            print(f"Warning: Error checking final question completion: {e}")
            return False

    def can_access_section(self, section_name):
        """Check if a section can be accessed"""
        if section_name not in self.sections:
            return False
        if section_name == self.sections[0]:  # First section is always accessible
            return True
        
        section_index = self.sections.index(section_name)
        previous_section = self.sections[section_index - 1]
        
        # Check if the final question of the previous section is completed
        return self.is_section_final_question_completed(previous_section)

    def can_access_question(self, section_name, question_id):
        """Check if a question can be accessed"""
        if not self.can_access_section(section_name):
            return False
        
        if self._is_optional_question(section_name, question_id):
            return True
        
        question_sequence = self.question_sequences.get(section_name, [])
        if not question_sequence:
            return True
        
        try:
            question_index = question_sequence.index(question_id)
        except ValueError:
            return True
        
        if question_index == 0:
            return True
        
        previous_question = question_sequence[question_index - 1]
        completed_questions = self._safe_get("completed_questions", {})
        section_questions = completed_questions.get(section_name, [])
        
        return previous_question in section_questions
    
    def _is_optional_question(self, section_name, question_id):
        """Check if a question is optional (always accessible)"""
        # Optional questions are identified by "optional" in their question ID
        # This makes the system generalizable and maintainable
        return "optional" in question_id.lower()
    
    def can_access_text_after_question(self, section_name, question_id):
        """Check if text content after a specific question should be visible"""
        # Text after a question is visible if the question is accessible
        # For optional questions, text is always visible
        if self._is_optional_question(section_name, question_id):
            return True
        return self.can_access_question(section_name, question_id)
    
    def get_progress_summary(self):
        """Get a summary of student's progress"""
        try:
            completed_sections = self._safe_get("completed_sections", set())
            total_sections = len(self.sections)
            completed_count = len(completed_sections)
            
            return {
                "total_sections": total_sections,
                "completed_sections": completed_count,
                "progress_percentage": round((completed_count / total_sections) * 100, 1),
                "next_section": self.sections[completed_count] if completed_count < total_sections else None
            }
        except Exception as e:
            print(f"Warning: Error getting progress summary: {e}")
            return {"total_sections": 0, "completed_sections": 0, "progress_percentage": 0, "next_section": None}
    
    def record_optional_response(self, question_id, response):
        """Record a response to an optional question"""
        try:
            self._ensure_session_state()
            if "optional_responses" not in st.session_state[self.session_key]:
                st.session_state[self.session_key]["optional_responses"] = {}
            st.session_state[self.session_key]["optional_responses"][question_id] = response
        except Exception as e:
            print(f"Warning: Error recording optional response: {e}")
    
    def record_attempt(self, question_id, is_correct, answer_given=None, section_name=None):
        """Record an attempt at a question"""
        try:
            self._ensure_session_state()
            
            # Initialize trials if not exists
            if "trials" not in st.session_state[self.session_key]:
                st.session_state[self.session_key]["trials"] = {}
            
            # Initialize question data if not exists
            if question_id not in st.session_state[self.session_key]["trials"]:
                st.session_state[self.session_key]["trials"][question_id] = {
                    "attempts": 0,
                    "correct_attempts": 0,
                    "incorrect_attempts": 0,
                    "answers_given": [],
                    "first_correct_attempt": None,
                    "section": section_name
                }
            
            trial_data = st.session_state[self.session_key]["trials"][question_id]
            trial_data["attempts"] += 1
            
            if is_correct:
                trial_data["correct_attempts"] += 1
                if trial_data["first_correct_attempt"] is None:
                    trial_data["first_correct_attempt"] = trial_data["attempts"]
                
                # Mark question as complete
                if section_name:
                    self.mark_question_complete(section_name, question_id)
                    
                    # Check if this is the final question of the section
                    question_sequence = self.question_sequences.get(section_name, [])
                    if question_sequence and question_id == question_sequence[-1]:
                        # This is the final question, mark section complete
                        self.mark_section_complete(section_name)
            else:
                trial_data["incorrect_attempts"] += 1
            
            if answer_given is not None:
                trial_data["answers_given"].append(answer_given)
                
        except Exception as e:
            print(f"Warning: Error recording attempt: {e}")
    
    def get_attempts_for_question(self, question_id):
        """Get the number of attempts for a specific question"""
        try:
            trials = self._safe_get("trials", {})
            if question_id in trials:
                return trials[question_id]["attempts"]
            return 0
        except Exception as e:
            print(f"Warning: Error getting attempts for question: {e}")
            return 0
    
    def get_trials_until_correct(self, question_id):
        """Get the number of trials until the student got the question correct"""
        try:
            trials = self._safe_get("trials", {})
            if question_id in trials:
                trial_data = trials[question_id]
                if trial_data["first_correct_attempt"] is not None:
                    return trial_data["first_correct_attempt"]
            return None
        except Exception as e:
            print(f"Warning: Error getting trials until correct: {e}")
            return None
    
    def mark_session_complete(self):
        """Mark the session as complete"""
        self._safe_set("session_complete", True)
    
    def verify_csv_password(self, password):
        """Verify password for CSV download access"""
        config = self._load_password_config()
        return password == config.get("csv_download_password", "")
    
    def is_admin_email(self, email):
        """Check if email is in admin list"""
        config = self._load_password_config()
        admin_emails = config.get("admin_emails", [])
        return email.lower() in [admin.lower() for admin in admin_emails]
    
    def export_to_csv(self, filename=None, password=None):
        """Export the comprehensive trial data to a CSV file - one row per student"""
        # Check password if provided
        if password and not self.verify_csv_password(password):
            return None, "Incorrect password"
        
        # Check if user is admin or has valid password
        current_email = self.get_student_email()
        if not self.is_admin_email(current_email) and not password:
            return None, "Password required for CSV download"
        
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"student_trials_{timestamp}.csv"
            
            # Get safe values
            student_id = self.get_student_id()
            email = self.get_student_email()
            session_start_time = self._safe_get("start_time", datetime.now().isoformat())
            session_complete = self._safe_get("session_complete", False)
            
            # Create one row per student with all data
            student_row = {
                "student_id": student_id,
                "email": email,
                "session_start_time": session_start_time,
                "session_complete": session_complete,
                "export_time": datetime.now().isoformat(),
                "total_questions_attempted": 0,
                "total_attempts": 0,
                "questions_correct": 0,
                "completion_rate": 0.0
            }
            
            # Add optional question responses
            optional_responses = self._safe_get("optional_responses", {})
            for question_id, response in optional_responses.items():
                if isinstance(response, list):
                    # Handle multiselect responses
                    student_row[f"optional_{question_id}"] = ", ".join(response)
                else:
                    student_row[f"optional_{question_id}"] = str(response)
            
            # Add regular question data
            trials = self._safe_get("trials", {})
            total_attempts = 0
            questions_correct = 0
            
            for question_id, trial_data in trials.items():
                # Add attempts for this question
                student_row[f"{question_id}_attempts"] = trial_data["attempts"]
                student_row[f"{question_id}_trials_to_correct"] = trial_data["first_correct_attempt"] or "Never correct"
                student_row[f"{question_id}_correct_attempts"] = trial_data["correct_attempts"]
                student_row[f"{question_id}_incorrect_attempts"] = trial_data["incorrect_attempts"]
                
                # Track totals
                total_attempts += trial_data["attempts"]
                if trial_data["first_correct_attempt"] is not None:
                    questions_correct += 1
            
            # Update summary statistics
            student_row["total_questions_attempted"] = len(trials)
            student_row["total_attempts"] = total_attempts
            student_row["questions_correct"] = questions_correct
            if len(trials) > 0:
                student_row["completion_rate"] = round((questions_correct / len(trials)) * 100, 1)
            
            # Create DataFrame with single row
            df = pd.DataFrame([student_row])
            
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            # Save to CSV
            csv_path = os.path.join("data", filename)
            df.to_csv(csv_path, index=False)
            
            return csv_path, "Success"
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None, f"Error: {str(e)}"
    
    def get_summary_stats(self):
        """Get summary statistics for the current session (for internal use only)"""
        try:
            trials = self._safe_get("trials", {})
            total_questions = len(trials)
            total_attempts = sum(trial["attempts"] for trial in trials.values())
            correct_questions = sum(1 for trial in trials.values() 
                                  if trial["first_correct_attempt"] is not None)
            
            return {
                "total_questions": total_questions,
                "total_attempts": total_attempts,
                "correct_questions": correct_questions,
                "questions_remaining": total_questions - correct_questions
            }
        except Exception as e:
            print(f"Error getting summary stats: {e}")
            return {
                "total_questions": 0,
                "total_attempts": 0,
                "correct_questions": 0,
                "questions_remaining": 0
            }
    
    def get_session_state(self):
        """Get the session state data - for debugging and direct access"""
        try:
            self._ensure_session_state()
            return st.session_state[self.session_key]
        except Exception as e:
            print(f"Error getting session state: {e}")
            return {}

# Global instance
trial_tracker = TrialTracker()
