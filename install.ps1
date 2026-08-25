<#
.SYNOPSIS
  grill-to-PRD 一键安装脚本：复制技能目录到 WorkBuddy 默认技能文件夹（或自定义目标）。

.DESCRIPTION
  把本 skill（grill-to-prd）安装为 WorkBuddy 用户级技能，日常可直接调用。
  安装前对比源版本（CHANGELOG 最新条目）与已安装副本版本，提示版本漂移（R1 教训）。
  兼容 Windows PowerShell 5.1 与 PowerShell 7（不用 && / 三元 / ?? 等 7+ 语法）。

.PARAMETER Target
  目标技能根目录（默认：$HOME\.workbuddy\skills）
  安装位置为 $Target\grill-to-prd

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\install.ps1
  powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target "D:\my-skills"
#>

[CmdletBinding()]
param(
    [string]$Target = ""
)

$ErrorActionPreference = "Stop"

# ---- 1. 定位源目录（脚本所在目录） ----
$Source = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceSkill = Join-Path $Source "SKILL.md"
if (-not (Test-Path $SourceSkill)) {
    Write-Host "[ERROR] 源目录缺少 SKILL.md: $SourceSkill" -ForegroundColor Red
    exit 1
}

# ---- 2. 确定目标目录 ----
if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Join-Path $HOME ".workbuddy\skills"
}
$Dest = Join-Path $Target "grill-to-prd"

# ---- 3. 读取版本（CHANGELOG 第一个版本条目） ----
function Get-VersionFromChangelog {
    param([string]$Path)
    $changelog = Join-Path $Path "CHANGELOG.md"
    if (-not (Test-Path $changelog)) { return "未知" }
    $line = Get-Content $changelog -TotalCount 20 | Where-Object { $_ -match '^## \[v' } | Select-Object -First 1
    if ($line -match '\[(v[0-9]+\.[0-9]+\.[0-9]+)\]') { return $Matches[1] }
    return "未知"
}

$SrcVersion = Get-VersionFromChangelog -Path $Source
$DestVersion = "（未安装）"
if (Test-Path (Join-Path $Dest "CHANGELOG.md")) {
    $DestVersion = Get-VersionFromChangelog -Path $Dest
}

Write-Host "== grill-to-PRD 安装 ==" -ForegroundColor Cyan
Write-Host "  源版本 : $SrcVersion"
Write-Host "  目标版本: $DestVersion"

if ($SrcVersion -ne "未知" -and $DestVersion -ne "（未安装）" -and $SrcVersion -ne $DestVersion) {
    Write-Host "  [WARN] 版本漂移：源 $SrcVersion != 已装 $DestVersion，将覆盖为源版本" -ForegroundColor Yellow
}

# ---- 4. 复制（排除 .git） ----
if (Test-Path $Dest) {
    Remove-Item $Dest -Recurse -Force
}
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Copy-Item -Path (Join-Path $Source "*") -Destination $Dest -Recurse -Force
if (Test-Path (Join-Path $Dest ".git")) {
    Remove-Item (Join-Path $Dest ".git") -Recurse -Force
}
if (Test-Path (Join-Path $Dest ".gitattributes")) {
    Remove-Item (Join-Path $Dest ".gitattributes") -Force
}
if (Test-Path (Join-Path $Dest ".gitignore")) {
    Remove-Item (Join-Path $Dest ".gitignore") -Force
}

# ---- 5. 完成 ----
Write-Host "  [OK] 已安装到: $Dest" -ForegroundColor Green
Write-Host "  使用：新会话中触发需求澄清/写 PRD/需求边界收敛/选型引导等场景即可自动调用；" -ForegroundColor Cyan
Write-Host "       或显式说明「用 grill-to-PRD 梳理需求」。" -ForegroundColor Cyan
