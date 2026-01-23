❯ Implement the following plan:                                                                                                                                                                                        
                                                                                                                                                                                                                       
  # Note Summary - Implementation Plan                                                                                                                                                                                 
                                                                                                                                                                                                                       
  ## Overview                                                                                                                                                                                                          
  A Python-based local application that monitors your Outlook inbox for self-sent emails with a specific subject pattern (e.g., `[Note] Title here`) and creates corresponding OneNote pages. Designed for future      
  extensibility to support task management and AI-powered brainstorming.                                                                                                                                               
                                                                                                                                                                                                                       
  ## Architecture Decision                                                                                                                                                                                             
  **Code-based Python solution** using Microsoft Graph API, running locally on your machine with optional scheduled execution via macOS launchd.                                                                       
                                                                                                                                                                                                                       
  ---                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ## Project Structure                                                                                                                                                                                                 
  ```                                                                                                                                                                                                                  
  note-summary/                                                                                                                                                                                                        
  ├── src/                                                                                                                                                                                                             
  │   ├── main.py                    # CLI entry point                                                                                                                                                                 
  │   ├── auth/                                                                                                                                                                                                        
  │   │   ├── graph_auth.py          # MSAL device code flow authentication                                                                                                                                            
  │   │   └── token_cache.py         # Token persistence                                                                                                                                                               
  │   ├── services/                                                                                                                                                                                                    
  │   │   ├── email_service.py       # Outlook email fetching                                                                                                                                                          
  │   │   └── onenote_service.py     # OneNote page creation                                                                                                                                                           
  │   ├── processors/                                                                                                                                                                                                  
  │   │   └── email_processor.py     # Email-to-note conversion                                                                                                                                                        
  │   ├── storage/                                                                                                                                                                                                     
  │   │   └── processed_tracker.py   # SQLite tracker (avoid duplicates)                                                                                                                                               
  │   └── utils/                                                                                                                                                                                                       
  │       └── config.py              # Configuration management                                                                                                                                                        
  ├── config/                                                                                                                                                                                                          
  │   ├── config.yaml                # User settings (gitignored)                                                                                                                                                      
  │   └── config.example.yaml        # Template                                                                                                                                                                        
  ├── data/                          # Token cache + SQLite DB (gitignored)                                                                                                                                            
  ├── scripts/                                                                                                                                                                                                         
  │   └── com.user.note-summary.plist  # launchd scheduled task                                                                                                                                                        
  ├── tests/
  │   ├── conftest.py               # Shared pytest fixtures
  │   ├── test_config.py            # Config loading tests
  │   ├── test_email_processor.py   # Email processing tests
  │   └── test_processed_tracker.py # SQLite tracker tests
  ├── requirements.txt
  └── pyproject.toml                                                                                                                                                                                                   
  ```                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ---                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ## Implementation Steps                                                                                                                                                                                              
                                                                                                                                                                                                                       
  ### Step 1: Azure App Registration (One-time Setup)
  1. Go to Azure Portal → App registrations → New registration
  2. Name: "Note Summary"
  3. Set "Allow public client flows" to Yes
  4. Add API permissions (delegated):
     - `Mail.Read`, `Mail.ReadWrite`
     - `Notes.Create`, `Notes.ReadWrite`
     - `User.Read`

  **Note (Corporate Environments):** If your organization uses Conditional Access policies,
  you may need IT to either exempt this app from device compliance requirements or register
  your device with Azure AD/Intune. Error code 53003 indicates a Conditional Access block.                                                                                                                                                                                                        
                                                                                                                                                                                                                       
  ### Step 2: Project Setup                                                                                                                                                                                            
  - Create directory structure                                                                                                                                                                                         
  - Set up Python virtual environment                                                                                                                                                                                  
  - Install dependencies: `msal`, `requests`, `pyyaml`                                                                                                                                                                 
  - Create configuration files                                                                                                                                                                                         
                                                                                                                                                                                                                       
  ### Step 3: Authentication Module                                                                                                                                                                                    
  - Implement MSAL device code flow (user-friendly CLI auth)                                                                                                                                                           
  - Token caching for persistence between runs                                                                                                                                                                         
                                                                                                                                                                                                                       
  ### Step 4: Email Service                                                                                                                                                                                            
  - Fetch emails matching subject pattern `[Note]`                                                                                                                                                                     
  - Filter for self-sent emails only                                                                                                                                                                                   
  - Support configurable lookback period                                                                                                                                                                               
                                                                                                                                                                                                                       
  ### Step 5: OneNote Service                                                                                                                                                                                          
  - List notebooks/sections                                                                                                                                                                                            
  - Create pages with HTML content                                                                                                                                                                                     
  - Auto-create notebook/section if missing                                                                                                                                                                            
                                                                                                                                                                                                                       
  ### Step 6: Email Processor                                                                                                                                                                                          
  - Extract title from subject (after `[Note]` prefix)                                                                                                                                                                 
  - Clean email HTML for OneNote compatibility                                                                                                                                                                         
  - Add metadata footer (received date)                                                                                                                                                                                
                                                                                                                                                                                                                       
  ### Step 7: Processed Email Tracker                                                                                                                                                                                  
  - SQLite database to track processed emails                                                                                                                                                                          
  - Prevents duplicate processing across runs                                                                                                                                                                          
                                                                                                                                                                                                                       
  ### Step 8: CLI Entry Point                                                                                                                                                                                          
  - `--auth-only`: Initial authentication                                                                                                                                                                              
  - `--list-notebooks`: Show available notebooks                                                                                                                                                                       
  - `--verbose`: Detailed logging                                                                                                                                                                                      
  - `--daemon`: Continuous monitoring mode                                                                                                                                                                             
                                                                                                                                                                                                                       
  ### Step 9: Scheduled Execution                                                                                                                                                                                      
  - Create launchd plist for automatic runs every 5 minutes                                                                                                                                                            
  - Install to `~/Library/LaunchAgents/`                                                                                                                                                                               
                                                                                                                                                                                                                       
  ---                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ## Configuration (config.yaml)                                                                                                                                                                                       
  ```yaml                                                                                                                                                                                                              
  azure:                                                                                                                                                                                                               
  client_id: "YOUR_CLIENT_ID"                                                                                                                                                                                          
  tenant_id: "YOUR_TENANT_ID"                                                                                                                                                                                          
                                                                                                                                                                                                                       
  email:                                                                                                                                                                                                               
  subject_pattern: "[Note]"                                                                                                                                                                                            
  lookback_hours: 24                                                                                                                                                                                                   
  mark_as_read: true                                                                                                                                                                                                   
                                                                                                                                                                                                                       
  onenote:                                                                                                                                                                                                             
  notebook_name: "Email Notes"                                                                                                                                                                                         
  section_name: "Captured Notes"                                                                                                                                                                                       
  ```                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ---                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ## Dependencies
  - `msal` - Microsoft authentication
  - `requests` - HTTP client for Graph API
  - `pyyaml` - Configuration parsing
  - `pytest` - Unit testing                                                                                                                                                                                   
                                                                                                                                                                                                                       
  ---                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ## Future Extensions (Architecture Ready)                                                                                                                                                                            
                                                                                                                                                                                                                       
  ### Task Management                                                                                                                                                                                                  
  - Add `[Task]` subject pattern support                                                                                                                                                                               
  - Parse due dates from email body                                                                                                                                                                                    
  - Store in SQLite tasks table (schema included)                                                                                                                                                                      
  - Integrate with macOS reminders                                                                                                                                                                                     
                                                                                                                                                                                                                       
  ### AI Brainstorming                                                                                                                                                                                                 
  - Add Anthropic/Claude integration                                                                                                                                                                                   
  - Summarize recent notes                                                                                                                                                                                             
  - Generate insights from accumulated notes                                                                                                                                                                           
  - Brainstorm with notes as context                                                                                                                                                                                   
                                                                                                                                                                                                                       
  ---                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
  ## Verification Plan
  1. **Unit tests**: Run `pytest tests/ -v` to verify core logic
  2. **Authentication test**: Run `python -m src.main --auth-only` and verify device code auth flow
  3. **Notebook discovery**: Run `python -m src.main --list-notebooks` to see OneNote structure
  4. **End-to-end test**: Send email with subject `[Note] Test note` to yourself, run the script, verify page created in OneNote
  5. **Duplicate prevention**: Run script again, verify same email not processed twice
  6. **Scheduled run**: Install launchd plist, verify automatic processing    