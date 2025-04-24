!macro customInit
  ; Check if Python is installed
  nsExec::ExecToStack 'python --version'
  Pop $0
  ${If} $0 != 0
    nsExec::ExecToStack 'python3 --version'
    Pop $0
    ${If} $0 != 0
      MessageBox MB_YESNO "Python is required but not found. Do you want to open the Python download page?" IDYES openPythonPage IDNO continuePython
      openPythonPage:
        ExecShell "open" "https://www.python.org/downloads/"
      continuePython:
    ${EndIf}
  ${EndIf}
  
  ; Check if MongoDB is installed
  nsExec::ExecToStack 'mongod --version'
  Pop $0
  ${If} $0 != 0
    MessageBox MB_YESNO "MongoDB is required but not found. Do you want to open the MongoDB download page?" IDYES openMongoDBPage IDNO continueMongoDB
    openMongoDBPage:
      ExecShell "open" "https://www.mongodb.com/try/download/community"
    continueMongoDB:
  ${EndIf}
!macroend

!macro customInstall
  ; Create a folder for MongoDB data
  CreateDirectory "$APPDATA\CS2-Esports-Tracker\mongodb-data"
  
  ; Run the dependency installer
  ExecWait '"$INSTDIR\CS2 Esports Tracker.exe" --install-deps'
!macroend