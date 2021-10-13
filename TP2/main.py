import matplotlib.pyplot as plt


# Fonction : Création d'une matrice à partir du fichier PGM d'une image
# Paramètres : file = nom du fichier
# Return : liste comportant la matrice, le nombre magique, les dimensions de l'image et la valeur maximale
def createMatrix(file):
    file = open(file, "r")
    lines = file.readlines();
    file.close()
    # lecture de la partie header
    magic_number = lines[0].rstrip()  # Récupération du nombre magique
    size = lines[2].split()  # Récupération des dimensions de l'image
    maximum_value = lines[3].rstrip()  # Récupération de l'intensité maximum

    matrix = []
    matrixR = [[] for x in range(int(size[1]))]
    matrixG = [[] for x in range(int(size[1]))]
    matrixB = [[] for x in range(int(size[1]))]

    # On créé une liste provisoire qui contient l'ensemble des valeurs des pixels à la suite
    translation_matrix = []
    for line in lines[4:]:
        translation_matrix.append(line.split())

    pixelCount = 0
    lineCount = 0
    iterator = 0

    for i in range(0, len(translation_matrix)):
        for j in range(0, len(translation_matrix[1])):
            if lineCount >= int(size[0]):
                lineCount = 0
                iterator += 1
            pixelCount += 1
            if pixelCount == 1:
                matrixR[iterator].append(translation_matrix[i][j])
            elif pixelCount == 2:
                matrixG[iterator].append(translation_matrix[i][j])
            elif pixelCount == 3:
                matrixB[iterator].append(translation_matrix[i][j])
                pixelCount = 0
                lineCount += 1

    matrix.append(matrixR)
    matrix.append(matrixG)
    matrix.append(matrixB)

    return [matrix, magic_number, size, maximum_value]


def createImage(matrix, file_name, magic_number, comments, width, height, maximum_value):
    fic = open(file_name, 'w')  # On ouvre le fichier PGM en écriture
    fic.write(magic_number + '\n')  # On note le format du fichier
    fic.write('# ' + comments + '\n')  # Commentaires facultatifs
    fic.write(str(width) + ' ' + str(height) + '\n')  # On note ses dimensions
    if maximum_value != 0:
        fic.write(str(maximum_value) + '\n')  # On note la valeur de l'intensité maximale
    # On note les valeurs de la matrice
    for line in matrix:
        for value in line:
            fic.write(str(value) + ' ')
        fic.write('\n')
    fic.write('\n')
    fic.close()


def convertPPMtoPGM(matrixR, matrixG, matrixB):
    new_matrix = [[] for x in range(int(len(matrixR)))]
    max_value = 0
    for i in range(0, len(matrixR)):
        for j in range(0, len(matrixR[1])):
            final_value = int(matrixR[i][j]) / 3 + int(matrixG[i][j]) / 3 + int(matrixB[i][j]) / 3
            new_matrix[i].append(int(final_value))
            if final_value > max_value:
                max_value = int(final_value)

    return [new_matrix, max_value]


def calculateShine(matrix):
    intensity = 0
    for line in matrix:
        for value in line:
            intensity += value
    intensity = int(intensity / (len(matrix) * len(matrix[1])))

    return intensity


def calculateContrastVariation(matrix):
    maxValue = 0
    minValue = 255
    for line in matrix:
        for value in line:
            if value > maxValue:
                maxValue = value
            if value < minValue:
                minValue = value
    if maxValue == 0 and minValue == 0:
        variation = 0
    else:
        variation = int((maxValue - minValue) / (maxValue + minValue))
    return variation


def calculateContrastEcartType(matrix, shine):
    contrast = 0
    for line in matrix:
        for value in line:
            contrast += pow(value - shine, 2)
    contrast = int(pow(contrast / (len(matrix) * len(matrix[1])), 0.5))
    return contrast


def createHistogram(matrix, maxValue, name):
    histogramMatrix = [0 for x in range(maxValue + 1)]
    for line in matrix:
        for value in line:
            histogramMatrix[value] += 1
    plt.axis([0, len(histogramMatrix), 0, max(histogramMatrix)])
    plt.bar([x + 1 for x in range(0, len(histogramMatrix))], histogramMatrix)
    plt.savefig('histogram/' + name + '.png')
    plt.close()
    return histogramMatrix


def createCumulativeHistogram(histogramMatrix, name):
    for i in range(len(histogramMatrix)):
        if i > 0:
            histogramMatrix[i] += histogramMatrix[i - 1]
    plt.plot(histogramMatrix)
    plt.savefig('histogram/' + name + '.png')
    plt.close()
    return histogramMatrix


if __name__ == '__main__':
    # Question 6 :
    image_data = createMatrix('images/feep.ascii.ppm')
    image_data2 = createMatrix('images/snail.ascii.ppm')

    # Question 7 :
    createImage(image_data[0][0], 'matrixR.pgm', 'P2', 'PGM R File', image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data[0][1], 'matrixG.pgm', 'P2', 'PGM G File', image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data[0][2], 'matrixB.pgm', 'P2', 'PGM B File', image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data2[0][0], 'matrixR2.pgm', 'P2', 'PGM R File', image_data2[2][0],
                image_data2[2][1],
                image_data2[3])
    createImage(image_data2[0][1], 'matrixG2.pgm', 'P2', 'PGM G File', image_data2[2][0],
                image_data2[2][1],
                image_data2[3])
    createImage(image_data2[0][2], 'matrixB2.pgm', 'P2', 'PGM B File', image_data2[2][0],
                image_data2[2][1],
                image_data2[3])

    # Question 8 :
    convert_image_data = convertPPMtoPGM(image_data[0][0], image_data[0][1], image_data[0][2])
    convert_image_data2 = convertPPMtoPGM(image_data2[0][0], image_data2[0][1], image_data2[0][2])
    createImage(convert_image_data[0], 'convertPPMtoPGM.pgm', 'P2', 'conversion de PPM à PGM',
                len(convert_image_data[0][1]), len(convert_image_data[0]),
                convert_image_data[1])
    createImage(convert_image_data2[0], 'convertPPMtoPGM2.pgm', 'P2', 'conversion de PPM à PGM',
                len(convert_image_data2[0][1]), len(convert_image_data2[0]),
                convert_image_data2[1])

    # Question 9 :
    shine1 = calculateShine(convert_image_data[0])
    shine2 = calculateShine(convert_image_data2[0])

    # Question 10 :
    calculateContrastVariation(convert_image_data[0])
    calculateContrastVariation(convert_image_data2[0])

    # Question 11 :
    calculateContrastEcartType(convert_image_data[0], shine1)
    calculateContrastEcartType(convert_image_data2[0], shine2)

    # Question 12 :
    histogramMatrix1 = createHistogram(convert_image_data[0], convert_image_data[1], 'histogramMatrix1')
    createCumulativeHistogram(histogramMatrix1, 'cumulativeHistogramMatrix1')
    histogramMatrix2 = createHistogram(convert_image_data2[0], convert_image_data2[1], 'histogramMatrix2')
    createCumulativeHistogram(histogramMatrix2, 'cumulativeHistogramMatrix2')
