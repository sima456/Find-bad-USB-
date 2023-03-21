# Convert password to a secure string and export to file
$password = "MySecurePassword"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$securePassword | Export-CliXml -Path "C:\securepassword.xml"

# Disable Command Prompt through Registry
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\System" -Name "DisableCMD" -Value 1

# Import secure string from file and convert back to plain text
$securePassword = Import-CliXml -Path "C:\securepassword.xml"
$validPassword = ($securePassword | ConvertFrom-SecureString)

# Prompt for password when user wants to use Command Prompt
do {
    $password = Read-Host "Enter the password to use Command Prompt" -AsSecureString
    $passwordText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
} until ($passwordText -eq $validPassword)

# Enable Command Prompt through Registry
Remove-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\System" -Name "DisableCMD"
