# Uncertainty Hub - Flow Logic Documentation

## Overview
The Uncertainty Hub (`pages/01_Uncertainty_Hub.py`) is a comprehensive, progressive tutorial system for teaching error analysis and uncertainty concepts in physics lab settings. It implements a structured learning path with conditional access control, progress tracking, and adaptive content delivery.

## System Architecture

### Core Components

#### 1. Main Hub (`01_Uncertainty_Hub.py`)
- **Entry Point**: Central controller that manages the entire tutorial experience
- **Page Configuration**: Wide layout, expanded sidebar, ± icon
- **Session Management**: Handles user authentication and progress state

#### 2. Trial Tracker (`lib/trial_tracker.py`)
- **Progress Engine**: Manages student progress through sections and questions
- **Access Control**: Enforces sequential section completion
- **Data Persistence**: Tracks attempts, responses, and completion status
- **Export Functionality**: Provides CSV export for instructors (password protected)

#### 3. Section Modules (`pages/uncertainty_sections/`)
- **Modular Content**: Each section is a separate Python module
- **Conditional Rendering**: Content visibility depends on progress
- **Question Sequences**: Structured learning with progressive difficulty

## Flow Logic

### 1. Initialization & Authentication
```
User visits page → Email collection → Validation (@hamilton.edu) → Session initialization
```

**Key Features:**
- **Email Gate**: Must provide valid Hamilton College email to proceed
- **Session State**: Initializes trial tracker and progress tracking
- **Persistent State**: Progress maintained across page refreshes

### 2. Progress Tracking System

#### Section Access Control
```python
sections = [
    "intro", "precision_accuracy", "uncertainty_range", 
    "one_measurement", "range_method", "std_dev_gaussian", "standard_form"
]
```

**Access Rules:**
- **First Section**: Always accessible
- **Subsequent Sections**: Require completion of final question in previous section
- **Question Sequences**: Within each section, questions must be completed sequentially

#### Progress Calculation
```python
progress = {
    "total_sections": 7,
    "completed_sections": count,
    "progress_percentage": (completed / total) * 100,
    "next_section": next_unlocked_section
}
```

### 3. Navigation & UI

#### Tab System
- **Custom Styling**: Tabs look like traditional browser tabs
- **State Management**: Active tab stored in session state
- **Visual Feedback**: 
  - Active: Blue border, highlighted
  - Accessible: Clickable, normal appearance
  - Locked: Grayed out with 🔒 icon

#### Navigation Controls
- **Section Navigation**: "Next Section" button (only if accessible)
- **Scroll Management**: Automatic scroll-to-top on tab changes
- **Anchor System**: Reliable scrolling using HTML anchors

### 4. Content Delivery

#### Section Rendering
```python
def render_section_with_nav(section_index, render_callable):
    # Render section content
    render_callable()
    
    # Add navigation buttons
    # Back to Top, Next Section (if accessible)
```

#### Conditional Content
- **Question Visibility**: Based on completion of previous questions
- **Text Content**: Shows after required questions are completed
- **Optional Questions**: Always visible, don't block progress

### 5. Question System

#### Question Types
1. **Required Questions**: Must be completed to unlock next content
2. **Optional Questions**: Always accessible, for feedback/interest
3. **Final Questions**: Mark sections as complete when answered correctly

#### Answer Tracking
```python
def record_attempt(question_id, is_correct, answer_given, section_name):
    # Track attempts, correct/incorrect counts
    # Mark questions as complete
    # Mark sections as complete if final question
```

### 6. Data Management

#### Session State Structure
```python
session_state = {
    "trials": {},                    # Question attempt data
    "start_time": "ISO timestamp",
    "student_id": "auto-generated",
    "email": "hamilton.edu address",
    "optional_responses": {},        # Optional question answers
    "session_complete": False,
    "completed_sections": set(),     # Section completion status
    "completed_questions": {},       # Question completion status
    "current_section": None,
    "current_question": None
}
```

#### Export System
- **Password Protection**: CSV export requires instructor password
- **Student Data**: One row per student with comprehensive attempt data
- **Privacy**: Only accessible to authorized users

## Section-Specific Logic

### 1. Introduction (`01_intro.py`)
- **Optional Questions**: Understanding assessment, topic interests
- **Required Question**: "Do physicists care about uncertainty?" (Yes/No)
- **Unlock Condition**: Correct answer unlocks "Precision & Accuracy"

### 2. Precision & Accuracy (`02_precision_accuracy.py`)
- **Question Sequence**: 8 questions (pa_q1 through pa_q8)
- **Unlock Condition**: pa_q8 must be completed correctly
- **Content**: Distinguishing precision vs. accuracy concepts

### 3. Uncertainty as Range (`03_uncertainty_range.py`)
- **Question Sequence**: 4 questions (uncertainty_q1 through uncertainty_q4)
- **Unlock Condition**: uncertainty_q4 must be completed correctly
- **Content**: Range-based uncertainty estimation

### 4. One Measurement (`04_one_measurement.py`)
- **Question Sequence**: 2 questions (om_q1, om_q2)
- **Unlock Condition**: om_q2 must be completed correctly
- **Content**: Single measurement uncertainty

### 5. Range Method (`05_range_method.py`)
- **Question Sequence**: 2 questions (range_q1, range_q2)
- **Unlock Condition**: range_q2 must be completed correctly
- **Content**: Multiple measurement range method

### 6. Standard Deviation & Gaussian (`06_std_dev_gaussian.py`)
- **Question Sequence**: 5 questions (sd_q1 through sd_q5)
- **Unlock Condition**: sd_q5 must be completed correctly
- **Content**: Statistical uncertainty methods

### 7. Standard Form (`07_standard_form.py`)
- **Question Sequence**: 4 questions (sf_q1 through sf_q4)
- **Unlock Condition**: sf_q4 must be completed correctly
- **Content**: Scientific notation and uncertainty reporting

## Key Features

### 1. Progressive Learning
- **Sequential Access**: Students must master concepts before advancing
- **Adaptive Difficulty**: Questions build upon previous knowledge
- **Completion Tracking**: Clear progress indicators

### 2. Flexible Assessment
- **Multiple Attempts**: Students can retry questions
- **Attempt Tracking**: Records all attempts for analysis
- **Optional Feedback**: Collects student interests and understanding

### 3. Instructor Tools
- **Progress Monitoring**: Track individual student progress
- **Data Export**: CSV format for analysis
- **Password Protection**: Secure access to student data

### 4. User Experience
- **Responsive Design**: Wide layout with organized content
- **Visual Feedback**: Clear success/error messages
- **Navigation Aids**: Back to top, next section buttons

## Technical Implementation

### 1. State Management
- **Streamlit Session State**: Persistent across interactions
- **Safe Access**: Error handling for all state operations
- **Initialization**: Lazy loading of session data

### 2. Module System
- **Dynamic Imports**: Sections loaded at runtime
- **Path Management**: Relative imports for portability
- **Error Handling**: Graceful fallbacks for missing modules

### 3. Data Persistence
- **Local Storage**: Session data maintained in browser
- **Export Format**: Structured CSV with comprehensive metrics
- **Privacy Controls**: Email validation and access restrictions

## Usage Flow

### Student Experience
1. **Enter Email**: Provide @hamilton.edu address
2. **Navigate Sections**: Use tab system to move between topics
3. **Answer Questions**: Complete required questions to unlock next sections
4. **Track Progress**: Monitor completion in sidebar
5. **Optional Feedback**: Provide additional insights if desired

### Instructor Experience
1. **Monitor Progress**: View student completion rates
2. **Export Data**: Download CSV with password protection
3. **Analyze Performance**: Review question difficulty and student patterns
4. **Customize Content**: Modify section modules as needed

## Extension Points

### 1. New Sections
- Add to `sections` list in trial tracker
- Create new module in `uncertainty_sections/`
- Import in main hub
- Update question sequences

### 2. Question Types
- Extend `record_attempt` for new question formats
- Add validation logic for different answer types
- Implement custom scoring systems

### 3. Assessment Methods
- Add new progress metrics
- Implement adaptive difficulty
- Create personalized learning paths

This system provides a robust foundation for structured physics education with comprehensive progress tracking and flexible content delivery.
