# just use
# \Documents\WindowsPowerShell\Modules

$DocPath = [Environment]::GetFolderPath("MyDocuments")
Copy-Item -recurse ./PowerForensics  $DocPath/WindowsPowerShell/Modules -force
Import-Module PowerForensics

# Service
# Reg
function MGet-Reg{
    REG EXPORT HKEY_USERS          ./test/src/fileinfo/data/Registry/HKEY_USERS.reg
    REG EXPORT HKEY_CURRENT_USER   ./test/src/fileinfo/data/Registry/HKEY_CURRENT_USERS.reg
    REG EXPORT HKEY_CURRENT_CONFIG ./test/src/fileinfo/data/Registry/HKEY_CURRENTCONFIG.reg
    REG EXPORT HKEY_LOCAL_MACHINE  ./test/src/fileinfo/data/Registry/HKEY_LOCAL_MACHINE.reg
    REG EXPORT HKEY_CLASSES_ROOT   ./test/src/fileinfo/data/Registry/HKEY_CLASSES_ROOT.reg
}
function MGet-Evt{
    #?
}
function MGet-Log{
    $start = Get-Date

    Get-EventLog Application | Export-Csv ./test/fileinfo/data/Log/ApplicationEventLog.csv -ENCODING "UTF8" -NoTypeInformation
    Get-EventLog System | Export-Csv ./test/fileinfo/data/Log/SystemEventLog.csv -ENCODING "UTF8" -NoTypeInformation
    Get-EventLog Security | Export-Csv ./test/fileinfo/data/Log/SecurityEventLog.csv -ENCODING "UTF8" -NoTypeInformation

    Get-MpThreatDetection | Export-Csv ./test/fileinfo/data/Log/WidowsDefenderLog.csv -ENCODING "UTF8" -NoTypeInformation
    Get-ScheduledTask | Export-Csv ./test/fileinfo/data/Log/ScheduledTaskLog.csv -ENCODING "UTF8" -NoTypeInformation
    Get-HotFix | Export-Csv ./test/fileinfo/data/Log/HotFix.csv -ENCODING "UTF8" -NoTypeInformation

    Get-History | Export-Csv ./test/fileinfo/data/Log/PowershellCommandHistoryLog.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_StartupCommand | Export-Csv ./test/fileinfo/data/Log/Win32_StartupCommand.csv -ENCODING "UTF8" -NoTypeInformation
    
    Get-WmiObject -Class Win32_NTLogEvent | Export-Csv ./test/fileinfo/data/Log/Win32_NTLogEvent.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_NTLogEventLog | Export-Csv ./test/fileinfo/data/Log/Win32_NTLogEventLog.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_SystemSetting | Export-Csv ./test/fileinfo/data/Log/Win32_SystemSetting.csv -ENCODING "UTF8" -NoTypeInformation
    
    $end = Get-Date
    $timespan = $end - $start
    $seconds = $timespan.TotalSeconds
    Write-Host "Get Log Info To ./test/fileinfo/data/Log, Time Used $seconds."
}

function MGet-FileAndDirectory{
    $start = Get-Date

    Get-WmiObject -Class Win32_Directory | Export-Csv ./test/fileinfo/data/Log/Win32_Directory.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SubDirectory | Export-Csv ./test/fileinfo/data/Log/Win32_SubDirectory.csv -ENCODING "UTF8" -NoTypeInformation    
    Get-WmiObject -Class Win32_DirectorySpecification | Export-Csv ./test/fileinfo/data/Log/Win32_DirectorySpecification.csv -ENCODING "UTF8" -NoTypeInformation
    
    Get-WmiObject -Class Win32_FileSpeication | Export-Csv ./test/fileinfo/data/Log/Win32_FileSpeication.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_MoveFileAction | Export-Csv ./test/fileinfo/data/Log/Win32_MoveFileAction.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_ImplementCategory | Export-Csv ./test/fileinfo/data/Log/Win32_ImplementCategory.csv -ENCODING "UTF8" -NoTypeInformation
    
    

    $end = Get-Date
    $timespan = $end - $start
    $seconds = $timespan.TotalSeconds
    Write-Host "Get File And Directory Info To ./test/fileinfo/data/Log, Time Used $seconds."
}

# Read The Service Infomation 60.99sec, Time Is So Long, How to Optimize
function MGet-Service {
    $start = Get-Date

    Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Export-Csv ./test/fileinfo/data/Service/StopedServices.csv -ENCODING "UTF8" -NoTypeInformation
    Get-Service | Where-Object {$_.Status -eq 'Running'} | Export-Csv ./test/fileinfo/data/Service/RunningServices.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_Service | Export-Csv ./test/fileinfo/data/Service/Win32_Service.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_TerminalService | Export-Csv ./test/fileinfo/data/Service/Win32_TerminalService.csv -ENCODING "UTF8" -NoTypeInformation    

    Get-WmiObject -Class Win32_BaseService | Export-Csv ./test/fileinfo/data/Service/Win32_BaseService.csv -ENCODING "UTF8" -NoTypeInformation    
    Get-WmiObject -Class Win32_ApplicationService | Export-Csv ./test/fileinfo/data/Service/Win32_ApplicationService.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SystemServices | Export-Csv ./test/fileinfo/data/Service/Win32_SystemServices.csv -ENCODING "UTF8" -NoTypeInformation
    
    Get-WmiObject -Class Win32_DependentService | Export-Csv ./test/fileinfo/data/Service/Win32_DependentService.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_LoadOrderGroupServiceMembers | Export-Csv ./test/fileinfo/data/Service/Win32_LoadOrderGroupServiceMembers.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_LoadOrderGroupServiceDependencies | Export-Csv ./test/fileinfo/data/Service/Win32_LoadOrderGroupServiceDependencies.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_ServiceSpecification | Export-Csv ./test/fileinfo/data/Service/Win32_ServiceSpecification.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_ServiceSpecificationService | Export-Csv ./test/fileinfo/data/Service/Win32_ServiceSpecificationService.csv -ENCODING "UTF8" -NoTypeInformation

    $end = Get-Date
    $timespan = $end - $start
    $seconds = $timespan.TotalSeconds
    Write-Host "Get Service Info To ./test/fileinfo/data/Service, Time Used $seconds."
}
#Read The Account Information 133.50sec
function MGet-AccountInfo {
    $start = Get-Date

    Get-WmiObject -Class Win32_LoggedOnUser | Export-Csv ./test/fileinfo/data/Account/Win32_LoggedOnUser.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_LogonSession | Export-Csv ./test/fileinfo/data/Account/Win32_LogonSession.csv -ENCODING "UTF8" -NoTypeInformation
    
    Get-WmiObject -Class Win32_SystemAccount | Export-Csv ./test/fileinfo/data/Account/Win32_SystemAccount.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_UserAccount | Export-Csv ./test/fileinfo/data/Account/Win32_UserAccount.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_UserProfile | Export-Csv ./test/fileinfo/data/Account/Win32_UserProfile.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_Group | Export-Csv ./test/fileinfo/data/Account/Win32_Group.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_GroupUser | Export-Csv ./test/fileinfo/data/Account/Win32_GroupUser.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_NTLogEventUser | Export-Csv ./test/fileinfo/data/Account/Win32_NTLogEventUser.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_NetworkLoginProfile | Export-Csv ./test/fileinfo/data/Account/Win32_NetworkLoginProfile.csv -ENCODING "UTF8" -NoTypeInformation

    $end = Get-Date
    $timespan = $end - $start
    $seconds = $timespan.TotalSeconds
    Write-Host "Get Account Info To ./test/fileinfo/data/Account, Time Used $seconds."

}

#Read The Process And Program Info, Time Need TOOOOOOOOOOO Long  817.371sec
function MGet-PP {
    $start = Get-Date

    Get-Process | SORT -Descending CPU | Export-Csv ./test/fileinfo/data/Process/Process.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_Thread | Export-Csv ./test/fileinfo/data/Process/Win32_Thread.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SystemProcesses | Export-Csv ./test/fileinfo/data/Process/Win32_SystemProcesses.csv -ENCODING "UTF8" -NoTypeInformation
    
    Get-WmiObject -Class Win32_InstalledProgramFramework | Export-Csv ./test/fileinfo/data/Process/Win32_InstalledProgramFramework.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_InstalledSoftwareElement | Export-Csv ./test/fileinfo/data/Process/Win32_InstalledSoftwareElement.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_InstalledStoreProgram | Export-Csv ./test/fileinfo/data/Process/Win32_InstalledStoreProgram.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_InstalledWin32Program | Export-Csv ./test/fileinfo/data/Process/Win32_InstalledWin32Program.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_LogicalProgramGroup | Export-Csv ./test/fileinfo/data/Process/Win32_LogicalProgramGroup.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_LogicalProgramGroupDirectory  | Export-Csv ./test/fileinfo/data/Process/Win32_LogicalProgramGroupDirectory.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_LogicalProgramGroupItem | Export-Csv ./test/fileinfo/data/Process/Win32_LogicalProgramGroupItem.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_LogicalProgramGroupItemDataFile | Export-Csv ./test/fileinfo/data/Process/Win32_LogicalProgramGroupItemDataFile.csv -ENCODING "UTF8" -NoTypeInformation

    Get-WmiObject -Class Win32_SoftwareElement  | Export-Csv ./test/fileinfo/data/Process/Win32_SoftwareElement.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SoftwareElementCheck  | Export-Csv ./test/fileinfo/data/Process/Win32_SoftwareElementCheck.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SoftwareElementAction  | Export-Csv ./test/fileinfo/data/Process/Win32_SoftwareElementAction.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SoftwareElementCondition | Export-Csv ./test/fileinfo/data/Process/Win32_SofterwareElementCondition.csv -ENCODING "UTF8" -NoTypeInformation
    Get-WmiObject -Class Win32_SoftwareElementResource | Export-Csv ./test/fileinfo/data/Process/Win32_SofterwareElementResource.csv -ENCODING "UTF8" -NoTypeInformation
   
    Get-WmiObject -Class Win32_LaunchCondition | Export-Csv ./test/fileinfo/data/Process/Win32_LaunchCondition.csv -ENCODING "UTF8" -NoTypeInformation

    $end = Get-Date
    $timespan = $end - $start
    $seconds = $timespan.TotalSeconds
    Write-Host "Get Account Info To ./test/fileinfo/data/Program, Time Used $seconds."
}
#Read Net Info
function MGet-Net{
    $start = Get-Date
    
    Get-DnsClientCache | Export-Csv ./test/fileinfo/data/Network/DnsClientCache.csv -encoding "UTF8"  -NoTypeInformation

    Get-NetRoute | Export-Csv ./test/fileinfo/data/Network/NetRoute.csv -encoding "UTF8"  -NoTypeInformation
    Get-NetIPAddress | Export-Csv ./test/fileinfo/data/Network/NetIPAddress.csv -encoding "UTF8"  -NoTypeInformation
    Get-NetAdapter | Export-Csv ./test/fileinfo/data/Network/NetAdapter.csv -encoding "UTF8"  -NoTypeInformation
    Get-NetTCPConnection | Export-Csv ./test/fileinfo/data/Network/NetTCPConnection.csv -encoding "UTF8"  -NoTypeInformation
    Get-NetUDPEndpoint | Export-Csv ./test/fileinfo/data/Network/NetUDPEndpoint.csv -encoding "UTF8"  -NoTypeInformation
    Get-VpnConnection | Export-Csv ./test/fileinfo/data/Network/VpnConnection.csv -encoding "UTF8"  -NoTypeInformation

    $end = Get-Date
    $timespan = $end - $start
    $seconds = $timespan.TotalSeconds
    Write-Host "Get Account Info To ./test/fileinfo/data/Network, Time Used $seconds."
}

#Read File SHA256 Hash
# Get-ChildItem -Recurse ..\ -Exclude *.log |
# Where-Object { $_.FullName -notmatch '\\excludedir($|\\)' } | Get-FileHash

# $end = Get-Date
# $timespan = $end - $start
# $seconds = $timespan.TotalSeconds
# Write-Host "Get All Info Was Done, Time Used $seconds."


#Web-Server or Other

#得到当前向磁盘写入的有哪些程序

#内存分析
