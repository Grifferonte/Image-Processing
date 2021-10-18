import matplotlib.pyplot as plt


# Fonction : Création d'une matrice à partir d'une image
# Paramètres : file = nom du fichier
# Return : liste comportant les 3 matrices R G et B, le nombre magique, les dimensions de l'image et la valeur maximale


def createMatrix(file):
    file = open(file, "r")
    lines = file.readlines();
    file.close()
    # lecture de la partie header
    magic_number = lines[0].rstrip()  # Récupération du nombre magique
    size = lines[2].split()  # Récupération des dimensions de l'image
    maximum_value = lines[3].rstrip()  # Récupération de l'intensité maximum

    # On créé une liste provisoire qui contient l'ensemble des valeurs des pixels à la suite
    translation_matrix = []
    for line in lines[4:]:
        translation_matrix.append(line.split())

    pixel_count = 0
    line_count = 0
    iterator = 0

    # On initialise les matrices des composantes RGB associées
    matrix = []
    matrix_r = [[] for x in range(int(size[1]))]
    matrix_g = [[] for x in range(int(size[1]))]
    matrix_b = [[] for x in range(int(size[1]))]

    # A partir de la 4ème ligne du fichier, on ajoute les éléments de la liste à la suite dans les 3 matrices R,
    # G et B (On ajoute le premier dans la matrice R, le deuxième dans la matrice G, le troisième dans la matrice B
    # et on boucle jusqu'à finir la liste)
    for i in range(0, len(translation_matrix)):
        for j in range(0, len(translation_matrix[1])):
            if line_count >= int(size[0]):
                line_count = 0
                iterator += 1
            pixel_count += 1
            if pixel_count == 1:
                matrix_r[iterator].append(translation_matrix[i][j])
            elif pixel_count == 2:
                matrix_g[iterator].append(translation_matrix[i][j])
            elif pixel_count == 3:
                matrix_b[iterator].append(translation_matrix[i][j])
                pixel_count = 0
                line_count += 1

    matrix.append(matrix_r)
    matrix.append(matrix_g)
    matrix.append(matrix_b)
    return [matrix, magic_number, size, maximum_value]


# Fonction : Création d'une nouvelle image
# Paramètres : matrix = matrice à ajouter, magic_number = nombre magique de l'image,
#           comments = commentaires sur l'image, width = largeur de l'image, height = hauteur de l'image,
#           maximum_value = intensité maximale
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


# Fonction : Conversion d'une matrice d'un fichier de type PPM en une matrice d'un fichier de type PGM Paramètres :
# matrix_r : matrice de la composante rouge, matrix_g : matrice de la composante verte, matrix_b : matrice de la
# composante bleue
# Return : la matrice d'un fichier de type PGM et sa valeur maximale
def convertPPMMatrixtoPGM(matrixR, matrixG, matrixB):
    new_matrix = [[] for x in range(int(len(matrixR)))]
    max_value = 0
    for i in range(0, len(matrixR)):
        for j in range(0, len(matrixR[1])):
            final_value = int(matrixR[i][j]) / 3 + int(matrixG[i][j]) / 3 + int(matrixB[i][j]) / 3
            new_matrix[i].append(int(final_value))
            if final_value > max_value:
                max_value = int(final_value)

    return [new_matrix, max_value]


# Fonction : Calcule la brillance de l'image
# Paramètres : matrix : matrice de l'image à calculer
# Return : Brillance de l'image
def calculateShine(matrix):
    shine = 0
    # On additionne l'ensemble des valeurs des pixels qu'on divise par sa hauteur*largeur
    for line in matrix:
        for value in line:
            shine += value
    shine = int(shine / (len(matrix) * len(matrix[1])))
    return shine


# Fonction : Calcule le contraste de l'image selon la variation maximale
# Paramètres : matrix : matrice de l'image à calculer
# Return : Contraste de l'image
def calculateContrastVariation(matrix):
    maxValue = -1
    minValue = -1
    # On cherche la valeur maximale et minimale des pixels dans une matrice donnée en parcourant toute la matrice et
    # on applique ensuite la formule de calcul du contraste selon la variation maximale
    for line in matrix:
        for value in line:
            if value > maxValue:
                maxValue = value
            if value < minValue or minValue == -1:
                minValue = value
    # On établit le cas particulier où le calcul du contraste serait impossible (division par zéro)
    if maxValue == 0 and minValue == 0:
        contrast = 0
    else:
        contrast = int((maxValue - minValue) / (maxValue + minValue))
    return contrast


# Fonction : Calcule le contraste de l'image selon l'écart type
# Paramètres : matrix : matrice de l'image à calculer, shine : brillance de l'image
# Return : Contraste de l'image
def calculateContrastEcartType(matrix, shine):
    contrast = 0
    # on applique la formule de calcul du contraste selon l'écart type
    for line in matrix:
        for value in line:
            contrast += pow(value - shine, 2)
    contrast = int(pow(contrast / (len(matrix) * len(matrix[1])), 0.5))
    return contrast

# Fonction : Calcule l'histogramme de l'image
# Paramètres : matrix : matrice de l'image à calculer, max_value = valeur maximale, name = nom du fichier png à sauvegarder
# Return : matrice de l'histogramme de l'image
def createHistogram(matrix, max_value, name):
    histogramMatrix = [0 for x in range(256)]
    for line in matrix:
        for value in line:
            histogramMatrix[value] += 1
    plt.axis([0, len(histogramMatrix), 0, max(histogramMatrix)])
    plt.bar([x + 1 for x in range(0, len(histogramMatrix))], histogramMatrix)
    plt.title(name)
    plt.savefig('histogram/' + name + '.png')
    plt.close()
    return histogramMatrix

# Fonction : Calcule l'histogramme cumulé de l'image
# Paramètres : matrix : matrice de l'histogramme de l'image, name = nom du fichier png à sauvegarder
# Return : matrice de l'histogramme cumulé de l'image
def createCumulativeHistogram(histogramMatrix, name):
    for i in range(len(histogramMatrix)):
        #A chaque indice de la matrice on rajoute la valeur de l'indice précédent
        if i > 0:
            histogramMatrix[i] += histogramMatrix[i - 1]
    plt.plot(histogramMatrix)
    plt.title(name)
    plt.savefig('histogram/' + name + '.png')
    plt.close()
    return histogramMatrix


if __name__ == '__main__':
    # Question 6 :
    image_data = createMatrix('images/feep.ascii.ppm')
    image_data2 = createMatrix('images/snail.ascii.ppm')

    # Question 7 :
    createImage(image_data[0][0], 'matrixR_feep.pgm', 'P2', 'PGM R File', image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data[0][1], 'matrixG_feep.pgm', 'P2', 'PGM G File', image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data[0][2], 'matrixB_feep.pgm', 'P2', 'PGM B File', image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data2[0][0], 'matrixR_snail.pgm', 'P2', 'PGM R File', image_data2[2][0],
                image_data2[2][1],
                image_data2[3])
    createImage(image_data2[0][1], 'matrixG_snail.pgm', 'P2', 'PGM G File', image_data2[2][0],
                image_data2[2][1],
                image_data2[3])
    createImage(image_data2[0][2], 'matrixB_snail.pgm', 'P2', 'PGM B File', image_data2[2][0],
                image_data2[2][1],
                image_data2[3])

    # Question 8 :
    convert_image_data = convertPPMMatrixtoPGM(image_data[0][0], image_data[0][1], image_data[0][2])
    convert_image_data2 = convertPPMMatrixtoPGM(image_data2[0][0], image_data2[0][1], image_data2[0][2])
    createImage(convert_image_data[0], 'convertPPMtoPGM_feep.pgm', 'P2', 'conversion de PPM à PGM',
                len(convert_image_data[0][1]), len(convert_image_data[0]),
                convert_image_data[1])
    createImage(convert_image_data2[0], 'convertPPMtoPGM2_snail.pgm', 'P2', 'conversion de PPM à PGM',
                len(convert_image_data2[0][1]), len(convert_image_data2[0]),
                convert_image_data2[1])

    # Question 9 :
    shine1 = calculateShine(convert_image_data[0])
    print("La brillance de l'image feep est de " + str(shine1))
    shine2 = calculateShine(convert_image_data2[0])
    print("La brillance de l'image snail est de " + str(shine2))

    # Question 10 :
    first_contrast_method1 = calculateContrastVariation(convert_image_data[0])
    print("Le contraste de l'image feep selon la variation maximale est de " + str(first_contrast_method1))
    first_contrast_method2 = calculateContrastVariation(convert_image_data2[0])
    print("Le contraste de l'image snail selon la variation maximale est de " + str(first_contrast_method2))

    # Question 11 :
    second_contrast_method1 = calculateContrastEcartType(convert_image_data[0], shine1)
    print("Le contraste de l'image feep selon l'écart type est de " + str(second_contrast_method1))
    second_contrast_method2 = calculateContrastEcartType(convert_image_data2[0], shine2)
    print("Le contraste de l'image snail selon l'écart type est de " + str(second_contrast_method2))

    # Question 12 :
    histogramMatrix1 = createHistogram(convert_image_data[0], convert_image_data[1], 'histogramMatrix_feep')
    createCumulativeHistogram(histogramMatrix1, 'cumulativeHistogramMatrix_feep')
    histogramMatrix2 = createHistogram(convert_image_data2[0], convert_image_data2[1], 'histogramMatrix_snail')
    createCumulativeHistogram(histogramMatrix2, 'cumulativeHistogramMatrix_snail')


