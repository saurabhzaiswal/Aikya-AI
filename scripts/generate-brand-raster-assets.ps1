[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceDirectory = Join-Path $repoRoot 'docs/brand-source/og'
$publicDirectory = Join-Path $repoRoot 'frontend/public'
$brandDirectory = Join-Path $publicDirectory 'brand'
$ogDirectory = Join-Path $publicDirectory 'og'

function New-RoundedRectanglePath {
    param([float]$X, [float]$Y, [float]$Width, [float]$Height, [float]$Radius)

    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $diameter = $Radius * 2
    $path.AddArc($X, $Y, $diameter, $diameter, 180, 90)
    $path.AddArc($X + $Width - $diameter, $Y, $diameter, $diameter, 270, 90)
    $path.AddArc($X + $Width - $diameter, $Y + $Height - $diameter, $diameter, $diameter, 0, 90)
    $path.AddArc($X, $Y + $Height - $diameter, $diameter, $diameter, 90, 90)
    $path.CloseFigure()
    return $path
}

function Draw-AikyaSymbol {
    param(
        [System.Drawing.Graphics]$Graphics,
        [float]$X,
        [float]$Y,
        [float]$Size,
        [System.Drawing.Color]$Primary,
        [System.Drawing.Color]$Secondary
    )

    $scale = $Size / 64
    $primaryPen = [System.Drawing.Pen]::new($Primary, 12 * $scale)
    $secondaryPen = [System.Drawing.Pen]::new($Secondary, 12 * $scale)
    $primaryPen.StartCap = $primaryPen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
    $secondaryPen.StartCap = $secondaryPen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
    $primaryPen.LineJoin = $secondaryPen.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round

    $leftPath = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $leftPath.StartFigure()
    $leftPath.AddLine([System.Drawing.PointF]::new($X + (30 * $scale), $Y + (13 * $scale)), [System.Drawing.PointF]::new($X + (20 * $scale), $Y + (13 * $scale)))
    $leftPath.AddBezier([System.Drawing.PointF]::new($X + (20 * $scale), $Y + (13 * $scale)), [System.Drawing.PointF]::new($X + (14 * $scale), $Y + (13 * $scale)), [System.Drawing.PointF]::new($X + (11 * $scale), $Y + (16 * $scale)), [System.Drawing.PointF]::new($X + (11 * $scale), $Y + (22 * $scale)))
    $leftPath.AddLine([System.Drawing.PointF]::new($X + (11 * $scale), $Y + (22 * $scale)), [System.Drawing.PointF]::new($X + (11 * $scale), $Y + (32 * $scale)))
    $leftPath.AddBezier([System.Drawing.PointF]::new($X + (11 * $scale), $Y + (32 * $scale)), [System.Drawing.PointF]::new($X + (11 * $scale), $Y + (38 * $scale)), [System.Drawing.PointF]::new($X + (14 * $scale), $Y + (41 * $scale)), [System.Drawing.PointF]::new($X + (20 * $scale), $Y + (41 * $scale)))
    $leftPath.AddLine([System.Drawing.PointF]::new($X + (20 * $scale), $Y + (41 * $scale)), [System.Drawing.PointF]::new($X + (30 * $scale), $Y + (41 * $scale)))
    $Graphics.DrawPath($primaryPen, $leftPath)

    $rightPath = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $rightPath.StartFigure()
    $rightPath.AddLine([System.Drawing.PointF]::new($X + (34 * $scale), $Y + (23 * $scale)), [System.Drawing.PointF]::new($X + (44 * $scale), $Y + (23 * $scale)))
    $rightPath.AddBezier([System.Drawing.PointF]::new($X + (44 * $scale), $Y + (23 * $scale)), [System.Drawing.PointF]::new($X + (50 * $scale), $Y + (23 * $scale)), [System.Drawing.PointF]::new($X + (53 * $scale), $Y + (26 * $scale)), [System.Drawing.PointF]::new($X + (53 * $scale), $Y + (32 * $scale)))
    $rightPath.AddLine([System.Drawing.PointF]::new($X + (53 * $scale), $Y + (32 * $scale)), [System.Drawing.PointF]::new($X + (53 * $scale), $Y + (42 * $scale)))
    $rightPath.AddBezier([System.Drawing.PointF]::new($X + (53 * $scale), $Y + (42 * $scale)), [System.Drawing.PointF]::new($X + (53 * $scale), $Y + (48 * $scale)), [System.Drawing.PointF]::new($X + (50 * $scale), $Y + (51 * $scale)), [System.Drawing.PointF]::new($X + (44 * $scale), $Y + (51 * $scale)))
    $rightPath.AddLine([System.Drawing.PointF]::new($X + (44 * $scale), $Y + (51 * $scale)), [System.Drawing.PointF]::new($X + (34 * $scale), $Y + (51 * $scale)))
    $Graphics.DrawPath($secondaryPen, $rightPath)

    $primaryBrush = [System.Drawing.SolidBrush]::new($Primary)
    $secondaryBrush = [System.Drawing.SolidBrush]::new($Secondary)
    $barOne = New-RoundedRectanglePath ($X + (25 * $scale)) ($Y + (27 * $scale)) (14 * $scale) (5 * $scale) (2.5 * $scale)
    $barTwo = New-RoundedRectanglePath ($X + (25 * $scale)) ($Y + (33 * $scale)) (14 * $scale) (5 * $scale) (2.5 * $scale)
    $Graphics.FillPath($primaryBrush, $barOne)
    $Graphics.FillPath($secondaryBrush, $barTwo)

    $barOne.Dispose(); $barTwo.Dispose(); $primaryBrush.Dispose(); $secondaryBrush.Dispose()
    $leftPath.Dispose(); $rightPath.Dispose(); $primaryPen.Dispose(); $secondaryPen.Dispose()
}

function Save-Jpeg {
    param([System.Drawing.Bitmap]$Bitmap, [string]$Path, [long]$Quality = 88)

    $encoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
    $parameters = [System.Drawing.Imaging.EncoderParameters]::new(1)
    $parameters.Param[0] = [System.Drawing.Imaging.EncoderParameter]::new([System.Drawing.Imaging.Encoder]::Quality, $Quality)
    $Bitmap.Save($Path, $encoder, $parameters)
    $parameters.Dispose()
}

function New-SocialCard {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Eyebrow,
        [string]$Title,
        [string]$Description
    )

    $sourceImage = [System.Drawing.Image]::FromFile($Source)
    try {
        $canvas = [System.Drawing.Bitmap]::new(1200, 630, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
        $graphics = [System.Drawing.Graphics]::FromImage($canvas)
        try {
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
            $graphics.DrawImage($sourceImage, 0, 0, 1200, 630)

            $overlay = [System.Drawing.Drawing2D.LinearGradientBrush]::new(
                [System.Drawing.Rectangle]::new(0, 0, 700, 630),
                [System.Drawing.Color]::FromArgb(248, 255, 255, 255),
                [System.Drawing.Color]::FromArgb(0, 255, 255, 255),
                [System.Drawing.Drawing2D.LinearGradientMode]::Horizontal
            )
            $graphics.FillRectangle($overlay, 0, 0, 700, 630)
            $overlay.Dispose()

            $ink = [System.Drawing.Color]::FromArgb(20, 24, 39)
            $muted = [System.Drawing.Color]::FromArgb(77, 86, 112)
            $primary = [System.Drawing.Color]::FromArgb(81, 71, 229)
            $secondary = [System.Drawing.Color]::FromArgb(13, 148, 136)
            $inkBrush = [System.Drawing.SolidBrush]::new($ink)
            $mutedBrush = [System.Drawing.SolidBrush]::new($muted)
            $primaryBrush = [System.Drawing.SolidBrush]::new($primary)
            $fontFamily = [System.Drawing.FontFamily]::new('Segoe UI')
            $brandFont = [System.Drawing.Font]::new($fontFamily, 18, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $eyebrowFont = [System.Drawing.Font]::new($fontFamily, 15, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $titleFont = [System.Drawing.Font]::new($fontFamily, 50, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
            $bodyFont = [System.Drawing.Font]::new($fontFamily, 21, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
            $taglineFont = [System.Drawing.Font]::new($fontFamily, 15, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)

            Draw-AikyaSymbol $graphics 70 51 42 $primary $secondary
            $graphics.DrawString('Aikya', $brandFont, $inkBrush, 124, 63)
            $graphics.FillRectangle($primaryBrush, 72, 127, 32, 4)
            $graphics.DrawString($Eyebrow.ToUpperInvariant(), $eyebrowFont, $primaryBrush, 72, 145)
            $graphics.DrawString($Title, $titleFont, $inkBrush, [System.Drawing.RectangleF]::new(68, 188, 520, 190))
            $graphics.DrawString($Description, $bodyFont, $mutedBrush, [System.Drawing.RectangleF]::new(72, 408, 500, 90))
            $graphics.DrawString('One World. One Understanding.', $taglineFont, $inkBrush, 72, 558)

            Save-Jpeg $canvas $Destination 88

            $brandFont.Dispose(); $eyebrowFont.Dispose(); $titleFont.Dispose(); $bodyFont.Dispose(); $taglineFont.Dispose()
            $fontFamily.Dispose(); $inkBrush.Dispose(); $mutedBrush.Dispose(); $primaryBrush.Dispose()
        }
        finally {
            $graphics.Dispose()
            $canvas.Dispose()
        }
    }
    finally {
        $sourceImage.Dispose()
    }
}

function New-AppIcon {
    param([int]$Size, [string]$Destination)

    $bitmap = [System.Drawing.Bitmap]::new($Size, $Size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $background = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(67, 56, 202))
        $tile = New-RoundedRectanglePath 0 0 $Size $Size ($Size * .265)
        $graphics.FillPath($background, $tile)
        Draw-AikyaSymbol $graphics ($Size * .12) ($Size * .12) ($Size * .76) ([System.Drawing.Color]::White) ([System.Drawing.Color]::FromArgb(94, 234, 212))
        $bitmap.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
        $tile.Dispose(); $background.Dispose()
    }
    finally {
        $graphics.Dispose(); $bitmap.Dispose()
    }
}

function New-TransparentMark {
    param([string]$Destination)

    $bitmap = [System.Drawing.Bitmap]::new(512, 512, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        Draw-AikyaSymbol $graphics 24 24 464 ([System.Drawing.Color]::FromArgb(81, 71, 229)) ([System.Drawing.Color]::FromArgb(13, 148, 136))
        $bitmap.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $graphics.Dispose(); $bitmap.Dispose()
    }
}

$cards = @(
    @{ Source = 'aikya-product-base.jpg'; Output = 'aikya-product.jpg'; Eyebrow = 'Product'; Title = "Understand what matters,`nin your language."; Description = "Private text and document translation,`nwith clear limits and real control." },
    @{ Source = 'aikya-product-base.jpg'; Output = 'aikya-features.jpg'; Eyebrow = 'Features'; Title = "Translation that respects`nthe work around the words."; Description = "Translate text and digital PDFs in one`nfocused, privacy-aware workspace." },
    @{ Source = 'aikya-product-base.jpg'; Output = 'aikya-pricing.jpg'; Eyebrow = 'Early access'; Title = "Start focused.`nGrow with understanding."; Description = "Honest MVP boundaries today, with room`nto grow when the product proves value." },
    @{ Source = 'aikya-knowledge-base.jpg'; Output = 'aikya-knowledge.jpg'; Eyebrow = 'Guides'; Title = "Knowledge should travel`nwithout losing meaning."; Description = "Practical guidance for calm, confident`nmultilingual work." },
    @{ Source = 'aikya-trust-base.jpg'; Output = 'aikya-trust.jpg'; Eyebrow = 'Trust'; Title = "Privacy is part`nof understanding."; Description = "Clear boundaries. Honest processing.`nControl that belongs to you." },
    @{ Source = 'aikya-trust-base.jpg'; Output = 'aikya-about.jpg'; Eyebrow = 'Our reason'; Title = "Built from one belief:`nunderstanding should be shared."; Description = "An independent product shaped around`nlanguage access, clarity, and respect." },
    @{ Source = 'aikya-blog-base.png'; Output = 'aikya-blog.jpg'; Eyebrow = 'Founder notes'; Title = "Notes from building`na calmer language product."; Description = "Product decisions, engineering tradeoffs,`nand lessons from the work." },
    @{ Source = 'aikya-blog-foundation-base.png'; Output = 'aikya-blog-foundation.jpg'; Eyebrow = 'Foundation'; Title = "The foundation before`nthe feature rush."; Description = "Why clear boundaries, architecture, and`ntrust come before product breadth." }
)

foreach ($card in $cards) {
    New-SocialCard `
        -Source (Join-Path $sourceDirectory $card.Source) `
        -Destination (Join-Path $ogDirectory $card.Output) `
        -Eyebrow $card.Eyebrow `
        -Title $card.Title `
        -Description $card.Description
}

New-AppIcon 32 (Join-Path $publicDirectory 'favicon-32x32.png')
New-AppIcon 180 (Join-Path $publicDirectory 'apple-touch-icon.png')
New-AppIcon 192 (Join-Path $brandDirectory 'aikya-app-icon-192.png')
New-AppIcon 512 (Join-Path $brandDirectory 'aikya-app-icon-512.png')
New-TransparentMark (Join-Path $brandDirectory 'aikya-mark.png')

Write-Output "Generated $($cards.Count) social cards and five raster brand assets."
