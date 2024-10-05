apt install golang zmap -y
go build scan.go
zmap -p8080 -q | ./scan 8080
ok