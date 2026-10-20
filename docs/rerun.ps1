# rerun.ps1 - rebuild the main results of paper 09 (arXiv survey rule) in order, using the folder's own code (code\README.md has the full order).
# Usage:   powershell -ExecutionPolicy Bypass -File D:\Research-Publishing\09-arxiv-survey-rule\depth\appendix\rerun.ps1 [-Level check|analysis|literature|harvest]
#   -Level check       (default, seconds): confirm D:, confirm the cached inputs exist, run the classifier's built-in self-tests. Writes nothing.
#   -Level analysis    (about 25 minutes of CPU, disk heavy on USB): classifier validation, net coverage check, then the full analysis; REWRITES results\tables, results\figures,
#                      results\analysis_output.md. Another agent may be editing results\ - only run this when you mean to regenerate them.
#   -Level literature  (about 1 hour, network, OpenAlex lookups backed off): re-run the literature map in bibliometrics\ from cached responses.
#   -Level harvest     PRINTS the harvesting commands (hours, network, arXiv API 5 s apart, resumable) and does not run them.
param([ValidateSet("check","analysis","literature","harvest")][string]$Level = "check")
$ErrorActionPreference = "Stop"
$Root = "D:\Research-Publishing\09-arxiv-survey-rule"
if (-not (Test-Path D:\)) { throw "D: is not mounted - stopping." }
Set-Location $Root
$SysPy = "C:\Users\seans\AppData\Local\Programs\Python\Python312\python.exe"   # standard library only, used for harvest/parse/classify
$VenvPy = "$Root\.venv\Scripts\python.exe"                                      # numpy, statsmodels, scipy, matplotlib, pypdf, used by analyze.py
if (-not (Test-Path $SysPy)) { $SysPy = "python" }

if ($Level -eq "check") {
    foreach ($f in "data\days.jsonl.gz","data\net.jsonl.gz","data\counts_core.json","data\labels\labels.csv","data\labels\sample_key.csv","code\classify.py","code\analyze.py","03-design.md") {
        if (Test-Path "$Root\$f") { Write-Host "present  $f" } else { Write-Warning "MISSING  $f" }
    }
    Write-Host "== classifier self-tests (rules v1.0, frozen 13 Oct 2026)"
    & $SysPy code\classify.py
}
elseif ($Level -eq "analysis") {
    & $SysPy code\validate.py            # -> results\classifier_validation.md, results\label_disagreements.csv
    & $SysPy code\check_net.py           # -> results\net_coverage.md
    & $VenvPy code\analyze.py            # -> results\tables, results\figures, results\analysis_output.md
}
elseif ($Level -eq "literature") {
    $BM = "$Root\bibliometrics"; $Pipe = "D:\Research-Publishing\_tools\biblio-venv\Scripts\python.exe"; $R = "C:\Program Files\R\R-4.5.3\bin\Rscript.exe"
    Push-Location "$BM\python"
    & $Pipe pipeline.py all
    & $Pipe handscreen09.py            # rewrites data\clean\manual_exclusions.csv (rules X1-X3)
    & $Pipe pipeline.py build
    Pop-Location
    Push-Location "$BM\R"
    & $R 01_build_M.R
    & $R 02_bibliometrix.R M.rds R ID "arXiv survey rule literature map" 2020,2024
    Pop-Location
    Push-Location "$BM\python"
    & $Pipe figures_py.py; & $Pipe vosviewer_export.py; & $Pipe notes09.py; & $Pipe evidence.py; & $Pipe make_docs.py
    & $Pipe D:\Research-Publishing\_tools\burst.py $BM
    Pop-Location
}
else {
    Write-Host @"
Harvest (NOT executed; resumable; run one at a time; arXiv API Terms of Use: one request at a time, at least 3 s apart):
  cd $Root
  python code\harvest_api.py days
  python code\harvest_api.py counts_core
  python code\harvest_api.py net
  python code\parse.py days ; python code\parse.py net
  python code\make_label_sample.py        # reproduces the same 400-paper sample
Ready-to-run but never run: python code\harvest_oai.py  (OAI-PMH, about 3 GB for cs; never together with harvest_api.py)
Before running, remove the contact e-mail from the User-Agent string at the top of code\harvest_api.py (it is currently there).
"@
}
