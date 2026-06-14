<#
.SYNOPSIS
  New Town Water-Electric Site - Validation Checker
.DESCRIPTION
  Checks: HTML syntax / internal links / CSS / Google backend integration
  Usage: .\validate.ps1
#>
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$allPass = $true
$enc = [System.Text.Encoding]::UTF8

function Pass  { Write-Host "  OK $($args[0])" -ForegroundColor Green }
function Fail  { Write-Host "  XX $($args[0])" -ForegroundColor Red; $script:allPass = $false }
function Warn  { Write-Host "  !! $($args[0])" -ForegroundColor Yellow }
function Info  { Write-Host "     $($args[0])" -ForegroundColor DarkGray }
function Head  { Write-Host "`n--- $($args[0]) ---" -ForegroundColor Cyan }

function ReadFile($path) {
  return [System.IO.File]::ReadAllText($path, $enc)
}

$htmlFiles = Get-ChildItem -Path $root -Filter *.html -Recurse | Where-Object {
  $_.FullName -notmatch 'node_modules|\.git' -and $_.Name -ne 'editor.html'
}
$htmlPaths = $htmlFiles | ForEach-Object { $_.FullName }
$htmlCount = $htmlPaths.Count

function NormalizePath($p) {
  $p = $p.Replace('/', '\')
  $parts = $p -split '\\'
  $result = New-Object System.Collections.ArrayList
  foreach ($part in $parts) {
    if ($part -eq '..') { if ($result.Count -gt 0) { $result.RemoveAt($result.Count - 1) } }
    elseif ($part -eq '.' -or $part -eq '') { continue }
    else { [void]$result.Add($part) }
  }
  return $result -join '\'
}

function DecodeUrl($s) {
  if ($s -match '%[0-9A-Fa-f]{2}') {
    try { return [System.Uri]::UnescapeDataString($s) } catch { return $s }
  }
  return $s
}

$fileLookup = @{}
foreach ($fp in $htmlPaths) {
  $rel = $fp.Substring($root.Length).TrimStart('\')
  $key = NormalizePath $rel
  $fileLookup[$key.ToLowerInvariant()] = $fp
  $name = (Get-Item $fp).Name
  $nk = NormalizePath $name
  $fileLookup[$nk.ToLowerInvariant()] = $fp
}
$fileLookup['assets\styles.css'] = Join-Path $root 'assets\styles.css'

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Validation Report - $htmlCount HTML files" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# 1/4 HTML syntax
Head '1/4 HTML Syntax Check'
$headOpen = '<head(\s[^>]*)?>'
$headClose = '</head>'
$bodyOpen = '<body(\s[^>]*)?>'
$bodyClose = '</body>'
foreach ($fp in $htmlPaths) {
  $rel = $fp.Substring($root.Length).TrimStart('\')
  $content = ReadFile $fp
  $errors = @()
  if ($content -notmatch '<!doctype html>') { $errors += 'Missing DOCTYPE' }
  if ($content -notmatch '<html\s[^>]*lang=') { $errors += 'Missing lang attribute' }
  $hasCs = $content -match '<meta charset=' -or $content -match '<meta\s+[^>]*charset='
  if (-not $hasCs) { $errors += 'Missing charset' }
  $oh = ([regex]::Matches($content, $headOpen)).Count
  $ch = ([regex]::Matches($content, $headClose)).Count
  if ($oh -ne $ch) { $errors += "head unbalanced (open $oh / close $ch)" }
  $ob = ([regex]::Matches($content, $bodyOpen)).Count
  $cb = ([regex]::Matches($content, $bodyClose)).Count
  if ($ob -ne $cb) { $errors += "body unbalanced (open $ob / close $cb)" }
  if ($errors.Count -eq 0) { Pass $rel }
  else { Fail "$rel - $($errors -join '; ')" }
}

# 2/4 Internal links
Head '2/4 Internal Link Check'
$brokenLinks = @()
$checkedLinks = 0
foreach ($fp in $htmlPaths) {
  $rel = $fp.Substring($root.Length).TrimStart('\')
  $content = ReadFile $fp
  $sourceDir = Split-Path $rel -Parent
  if ($sourceDir -eq '.') { $sourceDir = '' }
  $m1 = [regex]::Matches($content, 'href\s*=\s*"([^"]+)"')
  $m2 = [regex]::Matches($content, "href\s*=\s*'([^']+)'")
  $hrefs = @()
  foreach ($m in $m1) { $hrefs += $m.Groups[1].Value }
  foreach ($m in $m2) { $hrefs += $m.Groups[1].Value }
  $skipPat = '^(https?://|mailto:|tel:|#|javascript:)'
  foreach ($href in $hrefs) {
    if ($href -match $skipPat) { continue }
    if ([string]::IsNullOrWhiteSpace($href)) { continue }
    $checkedLinks++
    $decoded = DecodeUrl $href
    if ($decoded -match '^/') { $np = NormalizePath $decoded.Substring(1) }
    elseif ($sourceDir -eq '') { $np = NormalizePath $decoded }
    else { $np = NormalizePath "$sourceDir\$decoded" }
    if (-not $fileLookup.ContainsKey($np.ToLowerInvariant())) { $brokenLinks += "[$rel] -> $href" }
  }
}
if ($brokenLinks.Count -eq 0) { Pass "All $checkedLinks internal links valid" }
else {
  Fail "Found $($brokenLinks.Count) broken links:"
  foreach ($bl in $brokenLinks) { Info $bl }
}

# 3/4 CSS
Head '3/4 CSS Check'
$cssPath = Join-Path $root 'assets\styles.css'
if (Test-Path $cssPath) {
  Pass 'assets/styles.css exists'
  $cc = ReadFile $cssPath
  $obr = ([regex]::Matches($cc, '{')).Count
  $cbr = ([regex]::Matches($cc, '}')).Count
  if ($obr -eq $cbr) { Pass "CSS braces balanced ($obr rules)" }
  else { Fail "CSS braces unbalanced ($obr open / $cbr close)" }
  $vars = [regex]::Matches($cc, '--[\w-]+') | ForEach-Object { $_.Value } | Select-Object -Unique
  if ($vars.Count -gt 0) { Pass "Defined $($vars.Count) CSS variables" }
  else { Warn 'No CSS variables defined' }
  $vp = 'var\((--[\w-]+)\)'
  $uv = [regex]::Matches($cc, $vp) | ForEach-Object { $_.Groups[1].Value } | Select-Object -Unique
  $mv = $uv | Where-Object { $_ -notin $vars }
  if ($mv.Count -gt 0) { Fail "Undefined CSS variables: $($mv -join ', ')" }
  else { Pass 'All var() references match definitions' }
} else { Fail 'assets/styles.css not found!' }

# 4/4 Backend integration
Head '4/4 Backend Integration (Google Forms/Sheets)'
$fc = 0; $sc = 0; $ec = 0
$patForms = 'docs\.google\.com/forms/d/e/[A-Za-z0-9_-]+'
$patSheets = 'docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]+'
$patIframe = '<iframe\s[^>]*src\s*=\s*"([^"]+)"'
foreach ($fp in $htmlPaths) {
  $content = ReadFile $fp
  $fc += ([regex]::Matches($content, $patForms)).Count
  $sc += ([regex]::Matches($content, $patSheets)).Count
  $iframes = [regex]::Matches($content, $patIframe)
  foreach ($ifr in $iframes) {
    if ($ifr.Groups[1].Value -match 'docs\.google\.com') { $ec++ }
  }
}
if ($fc -gt 0) { Pass "Found $fc Google Forms links" } else { Warn 'No Google Forms links found' }
if ($sc -gt 0) { Pass "Found $sc Google Sheets links" } else { Warn 'No Google Sheets links found' }
if ($ec -gt 0) { Pass "Found $ec Google iframe embeds" } else { Warn 'No Google iframe embeds found' }

Write-Host "`n============================================" -ForegroundColor Cyan
if ($allPass) { Write-Host "  ALL CHECKS PASSED! Ready for git push" -ForegroundColor Green }
else { Write-Host "  SOME CHECKS FAILED - fix before git push" -ForegroundColor Red }
Write-Host "============================================" -ForegroundColor Cyan
exit $(if ($allPass) { 0 } else { 1 })