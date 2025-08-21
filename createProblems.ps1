# Define the content to be written in each file
$content = @"
\begin{Pro}
\end{Pro}

\begin{proof}
    \hspace{5mm}
\end{proof}
"@

#Create image directory
$directory = ".\images"

#create code directory
$directory = ".\code"

# Create the directory if it doesn't exist
$directory = ".\problems"
if (-Not (Test-Path -Path $directory)) {
    New-Item -ItemType Directory -Path $directory
}

# Create and write content to each file
for ($i = 1; $i -le 5; $i++) {
    $fileName = "$directory\p$i.tex"
    Set-Content -Path $fileName -Value $content
}

