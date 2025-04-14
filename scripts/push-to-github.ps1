Write-Host "Dang them thay doi..."
git add .

$commitMsg = Read-Host "Nhap noi dung commit"
git commit -m "$commitMsg"

Write-Host "Dang push len GitHub..."
git push -u origin main

Write-Host "Da cap nhat len GitHub thanh cong!"
