#requires -Version 7.3
param([Parameter(Mandatory)][string]$OutputDir,[Parameter(Mandatory)][string]$BuildDir,[switch]$SkipTests)
$ErrorActionPreference='Stop'
$OutputDir=[IO.Path]::GetFullPath($OutputDir)
$BuildDir=[IO.Path]::GetFullPath($BuildDir)
New-Item -ItemType Directory -Path "$BuildDir/native-slides" -Force | Out-Null
New-Item -ItemType Directory -Path "$BuildDir/native-sheets" -Force | Out-Null
$pptPath=Join-Path $OutputDir 'thu-nghiem-chuyen-can.pptx'
$pdfPath=Join-Path $OutputDir 'thu-nghiem-chuyen-can.pdf'
$xlsxPath=Join-Path $OutputDir 'tong-hop-chuyen-can.xlsx'
$receipt=[ordered]@{powerpoint_opened=$false;pdf_exported_from_actual_pptx=$false;slides=@();excel_opened=$false;tests=@()}
$pptExisting=@(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue)
$papp=New-Object -ComObject PowerPoint.Application
$pdeck=$null
try {
 $pdeck=$papp.Presentations.Open($pptPath,-1,0,0)
 $receipt.powerpoint_opened=$true
 for($i=1;$i -le $pdeck.Slides.Count;$i++){
  $sl=$pdeck.Slides.Item($i)
  $sl.Export((Join-Path "$BuildDir/native-slides" ("slide-{0:d2}.png" -f $i)),'PNG',1280,720)
  $text=New-Object System.Collections.Generic.List[string]
  $nativeCharts=0;$nativeTables=0
  for($j=1;$j -le $sl.Shapes.Count;$j++){
   $sh=$sl.Shapes.Item($j)
   if($sh.HasTextFrame -and $sh.TextFrame.HasText){$text.Add($sh.TextFrame.TextRange.Text)}
   if($sh.HasChart -eq -1){$nativeCharts++}
   if($sh.HasTable -eq -1){$nativeTables++;for($r=1;$r -le $sh.Table.Rows.Count;$r++){for($c=1;$c -le $sh.Table.Columns.Count;$c++){$text.Add($sh.Table.Cell($r,$c).Shape.TextFrame.TextRange.Text)}}}
  }
  $receipt.slides+=@{slide=$i;native_charts=$nativeCharts;native_tables=$nativeTables;text=$text.ToArray()}
 }
 $pdeck.SaveCopyAs($pdfPath,32)
 $receipt.pdf_exported_from_actual_pptx=Test-Path -LiteralPath $pdfPath
 if(-not $SkipTests){
  $copy=Join-Path $BuildDir 'editable-test.pptx'
  Copy-Item -LiteralPath $pptPath -Destination $copy
  $test=$papp.Presentations.Open($copy,0,0,0)
  try {
   $chartShape=$null
   for($j=1;$j -le $test.Slides.Item(2).Shapes.Count;$j++){if($test.Slides.Item(2).Shapes.Item($j).HasChart -eq -1){$chartShape=$test.Slides.Item(2).Shapes.Item($j);break}}
   $expectedWidth=[double]$chartShape.Width*0.9
   $chartShape.Width=$expectedWidth
   $excelBefore=@(Get-Process -Name EXCEL -ErrorAction SilentlyContinue)
   $chartShape.Chart.ChartData.Activate()
   $chartBook=$chartShape.Chart.ChartData.Workbook
   $chartExcel=$chartBook.Application
   $chartBook.Worksheets.Item(1).Cells.Item(2,2).Value2=0.12
   $chartBook.Worksheets.Item(1).Cells.Item(3,2).Value2=0.2
   $chartExcel.CalculateFullRebuild()
   $chartShape.Chart.SeriesCollection(1).Values=[double[]]@([double]$chartBook.Worksheets.Item(1).Cells.Item(2,2).Value2,[double]$chartBook.Worksheets.Item(1).Cells.Item(3,2).Value2)
   $chartShape.Chart.Refresh()
   $chartBook.Close($true)
   if($excelBefore.Count -eq 0 -and $chartExcel.Workbooks.Count -eq 0){$chartExcel.Quit()}
   $chartShape.Chart.Refresh()
   $test.Slides.Item(1).Shapes.Item(1).TextFrame.TextRange.Text='Kiểm tra chỉnh sửa riêng'
   $test.Save()
  } finally {$test.Close()}
  $test=$papp.Presentations.Open($copy,-1,0,0)
  try {
   $chartShape=$null
   for($j=1;$j -le $test.Slides.Item(2).Shapes.Count;$j++){if($test.Slides.Item(2).Shapes.Item($j).HasChart -eq -1){$chartShape=$test.Slides.Item(2).Shapes.Item($j);break}}
   $values=@($chartShape.Chart.SeriesCollection(1).Values)
   if([Math]::Abs([double]$chartShape.Width-$expectedWidth) -gt 0.01 -or [Math]::Abs([double]$values[0]-0.12) -gt 1e-10){throw 'Native chart edit/save/reopen failed'}
   if($test.Slides.Item(1).Shapes.Item(1).TextFrame.TextRange.Text -ne 'Kiểm tra chỉnh sửa riêng'){throw 'Native text edit/save/reopen failed'}
   $test.Slides.Item(2).Export((Join-Path $BuildDir 'edited-chart-test.png'),'PNG',1280,720)
   $receipt.tests+=@{test='PowerPoint embedded workbook cell edits with explicit series synchronization, resize and text edit/save/reopen on disposable copy';passed=$true;limit='Automatic chart-cache refresh after direct COM workbook cell edits was not established. The test explicitly synchronized series values from edited cells.'}
  } finally {$test.Close()}
 }
} finally {
 if($null -ne $pdeck){$pdeck.Close()}
 if($pptExisting.Count -eq 0 -and $papp.Presentations.Count -eq 0){$papp.Quit()}
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($papp)
}
$excel=New-Object -ComObject Excel.Application
$book=$null
try {
 $excel.Visible=$false
 $excel.DisplayAlerts=$false
 $book=$excel.Workbooks.Open($xlsxPath,0,$true)
 $receipt.excel_opened=$true
 $excel.CalculateFullRebuild()
 $main=$book.Worksheets.Item('Tong hop')
 $receipt.main_values=$main.Range('A6:I20').Value2
 if(-not $SkipTests){
  $before=[double]$main.Range('C37').Value2
  $main.Range('B29').Value2=14
  $excel.CalculateFullRebuild()
  $after=[double]$main.Range('C37').Value2
  if($before -ne 60 -or $after -ne 56){throw "Capacity recalc failed: $before / $after"}
  $receipt.tests+=@{test='capacity input 15 to 14';before=$before;after=$after;expected_after=56;passed=$true}
  $main.Range('B29').Value2=15
  $excel.CalculateFullRebuild()
  if([double]$main.Range('C37').Value2 -ne 60){throw 'Capacity restore failed'}
  $src=$book.Worksheets.Item('Nguon');$local=$book.Worksheets.Item('Dia ban')
  foreach($pair in @(@(8,7),@(160,159),@(311,310))){
   $rr=$pair[0];$dr=$pair[1]
   $count=[double]$src.Range("G$rr").Value2
   $enrol=[double]$src.Range("E$rr").Value2
   $src.Range("G$rr").Value2=$count+1
   $excel.CalculateFullRebuild()
   $calc=[double]$local.Range("E$dr").Value2
   if([Math]::Abs($calc-(($count+1)/$enrol)) -gt 1e-12){throw "PA input recalc failed at source $rr"}
   $src.Range("G$rr").Value2=$count
   $excel.CalculateFullRebuild()
   $receipt.tests+=@{test="PA formula recalc source row $rr";passed=$true}
  }
 }
 $views=@(@('Tong hop','A1:I23','summary'),@('Tong hop','A25:I43','capacity'),@('Dia ban','A1:L15','local'),@('Nguon','A1:P16','source'))
 foreach($v in $views){
  $sh=$book.Worksheets.Item($v[0]);$sh.PageSetup.PrintArea=$v[1];$sh.PageSetup.Orientation=2;$sh.PageSetup.PaperSize=8;$sh.PageSetup.Zoom=$false;$sh.PageSetup.FitToPagesWide=1;$sh.PageSetup.FitToPagesTall=1
  $sh.ExportAsFixedFormat(0,(Join-Path "$BuildDir/native-sheets" ($v[2]+'.pdf')))
 }
 $receipt.sheet_names=@(for($i=1;$i -le $book.Worksheets.Count;$i++){$book.Worksheets.Item($i).Name})
 $receipt.final_capacity=[double]$main.Range('C37').Value2
} finally {
 if($null -ne $book){$book.Close($false)}
 $excel.Quit()
 [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath "$BuildDir/native-receipt.json" -Encoding utf8
Write-Output ('Office export and checks completed: '+$pdfPath)
