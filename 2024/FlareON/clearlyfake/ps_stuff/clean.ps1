Set-Variable -Name testnet_endpoint -Value (" ")
Set-Variable -Name _body -Value ('{"method":"eth_call","params":[{"to":"$address","data":"0x5c880fcb"}, BLOCK],"id":1,"jsonrpc":"2.0"}')Set-Variable -Name resp -Value ((Invoke-RestMethod -Method 'Post' -Uri $testnet_endpoint -ContentType "application/json" -Body $_body).result)
# Remove the '0x' prefix
Set-Variable -Name hexNumber -Value ($resp -replace '0x', '')
# Convert from hex to bytes (ensuring pairs of hex characters)
Set-Variable -Name bytes0 -Value (0..($hexNumber.Length / 2 - 1) | ForEach-Object {
    Set-Variable -Name startIndex -Value ($_ * 2)Set-Variable -Name endIndex -Value ($startIndex + 1)  [Convert]::ToByte($hexNumber.Substring($startIndex, 2), 16)
    }) 
Set-Variable -Name bytes1 -Value ([System.Text.Encoding]::UTF8.GetString($bytes0))
Set-Variable -Name bytes2 -Value ($bytes1.Substring(64, 188))
# Convert from base64 to bytes
Set-Variable -Name bytesFromBase64 -Value ([Convert]::FromBase64String($bytes2))
Set-Variable -Name resultAscii -Value ([System.Text.Encoding]::UTF8.GetString($bytesFromBase64))Set-Variable -Name hexBytes -Value ($resultAscii | ForEach-Object {'{0:X2}' -f $_  
    # Format each byte as two-digit hex with uppercase letters
})
Set-Variable -Name hexString -Value ($hexBytes -join ' ') #
Write-Output $hexStringSet-Variable -Name hexBytes -Value ($hexBytes -replace " ", "")
# Convert from hex to bytes (ensuring pairs of hex characters)
Set-Variable -Name bytes3 -Value (0..($hexBytes.Length / 2 - 1) | ForEach-Object {
    Set-Variable -Name startIndex -Value ($_ * 2)Set-Variable -Name endIndex -Value ($startIndex + 1)[Convert]::ToByte($hexBytes.Substring($startIndex, 2), 16)}
    )
Set-Variable -Name bytes5 -Value ([Text.Encoding]::UTF8.GetString($bytes3))
# Convert the key to bytes
Set-Variable -Name keyBytes -Value ([Text.Encoding]::ASCII.GetBytes("FLAREON24"))
# Perform the XOR operation
Set-Variable -Name resultBytes -Value (@())for (Set-Variable -Name i -Value (0); $i -lt $bytes5.Length; $i++) {Set-Variable -Name resultBytes -Value ($resultBytes + ($bytes5[$i] -bxor $keyBytes[$i % $keyBytes.Length])) }
# Convert the result back to a string (assuming ASCII encoding)
Set-Variable -Name resultString -Value ([System.Text.Encoding]::ASCII.GetString($resultBytes))
Set-Variable -Name command -Value ("tar -x --use-compress-program 'cmd /c echo $resultString > flag' -f flag")Invoke-Expression $command