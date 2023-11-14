package main

import (
	"fmt"
	"image"
	"os"
	"path/filepath"

	// "image/color"
	"math"
)

func getImgPath(namaFile string) string {
	currentDir, err := os.Getwd()
	if err != nil {
		fmt.Println("Error getting current directory:", err)
		return ""
	}

	pathFile := filepath.Join(currentDir, "test", namaFile)
	return pathFile
}

func getHSV(img image.Image) (hVal, sVal, vVal [][]float64) {
	bounds := img.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y

	hVal = make([][]float64, height)
	sVal = make([][]float64, height)
	vVal = make([][]float64, height)

	for i := 0; i < height; i++ {
		hVal[i] = make([]float64, width)
		sVal[i] = make([]float64, width)
		vVal[i] = make([]float64, width)
	}

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			r, g, b, _ := img.At(x, y).RGBA()
			normalizedR := float64(r) / 65535.0
			normalizedG := float64(g) / 65535.0
			normalizedB := float64(b) / 65535.0

			Cmin := math.Min(normalizedR, math.Min(normalizedG, normalizedB))
			Cmax := math.Max(normalizedR, math.Max(normalizedG, normalizedB))
			delta := Cmax - Cmin

			vVal[y][x] = 0
			if Cmax >= 0 && Cmax < 0.2 {
				vVal[y][x] = 0
			} else if Cmax >= 0.2 && Cmax < 0.7 {
				vVal[y][x] = 1
			} else if Cmax >= 0.7 && Cmax <= 1 {
				vVal[y][x] = 2
			}

			sVal[y][x] = 0
			if Cmax != 0 {
				sVal[y][x] = delta / Cmax
			}
			if sVal[y][x] >= 0 && sVal[y][x] < 0.2 {
				sVal[y][x] = 0
			} else if sVal[y][x] >= 0.2 && sVal[y][x] < 0.7 {
				sVal[y][x] = 1
			} else if sVal[y][x] >= 0.7 && sVal[y][x] <= 1 {
				sVal[y][x] = 2
			}

			hVal[y][x] = 0
			if delta != 0 {
				switch {
				case Cmax == normalizedR:
					hVal[y][x] = (60 * math.Mod(((normalizedG-normalizedB)/delta), 6))
				case Cmax == normalizedG:
					hVal[y][x] = (60 * (((normalizedB - normalizedR) / delta) + 2))
				case Cmax == normalizedB:
					hVal[y][x] = (60 * (((normalizedR - normalizedG) / delta) + 4))
				}
			}
			hVal[y][x] = (math.Max(0, math.Min(360, float64(hVal[y][x]))))

			if hVal[y][x] >= 316 && hVal[y][x] <= 360 || hVal[y][x] == 0 {
				hVal[y][x] = 0
			} else if hVal[y][x] >= 1 && hVal[y][x] <= 25 {
				hVal[y][x] = 1
			} else if hVal[y][x] >= 26 && hVal[y][x] <= 40 {
				hVal[y][x] = 2
			} else if hVal[y][x] >= 41 && hVal[y][x] <= 120 {
				hVal[y][x] = 3
			} else if hVal[y][x] >= 121 && hVal[y][x] <= 190 {
				hVal[y][x] = 4
			} else if hVal[y][x] >= 191 && hVal[y][x] <= 270 {
				hVal[y][x] = 5
			} else if hVal[y][x] >= 271 && hVal[y][x] <= 295 {
				hVal[y][x] = 6
			} else if hVal[y][x] >= 296 && hVal[y][x] <= 315 {
				hVal[y][x] = 7
			}
		}
	}

	return hVal, sVal, vVal
}

func dotProductVector(vector1, vector2 []float64) float64 {
	if len(vector1) != len(vector2) {
		// Handle error: vectors must have the same length
		return 0
	}

	var value float64
	for i := 0; i < len(vector1); i++ {
		value += vector1[i] * vector2[i]
	}

	return value
}

func vectorLength(vector []float64) float64 {
	var value float64

	for _, v := range vector {
		value += v * v
	}

	return math.Sqrt(value)
}

func cosineSimilarity(vectorImg1, vectorImg2 []float64) float64 {
	lengthImg1 := vectorLength(vectorImg1)
	lengthImg2 := vectorLength(vectorImg2)

	if lengthImg1 != 0 && lengthImg2 != 0 {
		return dotProductVector(vectorImg1, vectorImg2) / (lengthImg1 * lengthImg2)
	} else {
		return 0
	}
}

func flatten(slice [][]int) []int {
	var result []int
	for _, row := range slice {
		result = append(result, row...)
	}
	return result
}

func hsvHistogram(hVal, sVal, vVal [][]int) []int {
	hValFlat := flatten(hVal)
	sValFlat := flatten(sVal)
	vValFlat := flatten(vVal)

	// Combine values into a single value, e.g., 711, 120, etc.
	combinedValues := make([]int, len(hValFlat))
	for i := range hValFlat {
		combinedValues[i] = hValFlat[i]*100 + sValFlat[i]*10 + vValFlat[i]
	}

	customBins := []int{0, 1, 2, 10, 11, 12, 20, 21, 22, 100, 101, 102, 110, 111, 112, 120, 121, 122, 200, 201, 202, 210, 211, 212, 220, 221, 222, 300, 301, 302, 310, 311, 312, 320, 321, 322, 400, 401, 402, 410, 411, 412, 420, 421, 422, 500, 501, 502, 510, 511, 512, 520, 521, 522, 600, 601, 602, 610, 611, 612, 620, 621, 622, 700, 701, 702, 710, 711, 712, 720, 721, 722}

	frequencyDict := make(map[int]int)
	for _, value := range combinedValues {
		frequencyDict[value]++
	}

	var frequencyVector []int
	for _, key := range customBins {
		frequencyVector = append(frequencyVector, frequencyDict[key])
	}

	return frequencyVector
}

func main() {}

// // Example usage:
// namaFile := "5.jpg"
// imgPath := getImgPath(namaFile)
// fmt.Println("Image path:", imgPath)
// // Example usage with an image (replace this with your actual image loading)
// img := image.NewRGBA(imgPath)
// img.Set(0, 0, color.RGBA{255, 0, 0, 255})
// img.Set(1, 1, color.RGBA{0, 255, 0, 255})
// img.Set(2, 2, color.RGBA{0, 0, 255, 255})

// hVal, sVal, vVal := getHSV(img)

// fmt.Println("Hue:")
// fmt.Println(hVal)
// fmt.Println("Saturation:")
// fmt.Println(sVal)
// fmt.Println("Value:")
// fmt.Println(vVal)

// vector1 := []float64{1.0, 2.0, 3.0}
// vector2 := []float64{4.0, 5.0, 6.0}

// result := dotProductVector(vector1, vector2)
// fmt.Printf("Dot product: %.2f\n", result)
// fmt.Printf("Length 1: %.2f\n", vectorLength(vector1))
// fmt.Printf("Length 2: %.2f\n", vectorLength(vector2))
// fmt.Printf("Cosine Similarity: %.2f\n", cosineSimilarity(vector1, vector2))
// }
