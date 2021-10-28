# -*- coding: ISO-8859-1 -*-
import copy
import math


# Fonction : Cr�ation d'une nouvelle image
# Param�tres : matrix = matrice � ajouter, magic_number = nombre magique de l'image,
#           comments = commentaires sur l'image, width = largeur de l'image, height = hauteur de l'image,
#           maximum_value = intensit� maximale
def createImage(matrix, file_name, magic_number, comments, width, height, maximum_value):
    fic = open(file_name, 'w')  # On ouvre le fichier PGM en �criture
    fic.write(magic_number + '\n')  # On note le format du fichier
    fic.write('# ' + comments + '\n')  # Commentaires facultatifs
    fic.write(str(width) + ' ' + str(height) + '\n')  # On note ses dimensions
    if maximum_value != 0:
        fic.write(str(maximum_value) + '\n')  # On note la valeur de l'intensit� maximale
    # On note les valeurs de la matrice
    for line in matrix:
        for value in line:
            fic.write(str(value) + ' ')
        fic.write('\n')
    fic.write('\n')
    fic.close()


# Fonction : Cr�ation d'une matrice � partir du fichier PGM d'une image
# Param�tres : file = nom du fichier
# Return : liste comportant la matrice, le nombre magique, les dimensions de l'image et la valeur maximale
def createMatrix(file):
    file = open(file, "r")
    lines = file.readlines();
    file.close()
    # lecture de la partie header
    magic_number = lines[0].rstrip()  # R�cup�ration du nombre magique
    size = lines[2].split()  # R�cup�ration des dimensions de l'image
    maximum_value = lines[3].rstrip()  # R�cup�ration de l'intensit� maximum

    # On cr�� une liste provisoire qui contient l'ensemble des valeurs des pixels � la suite
    translation_matrix = []
    for line in lines[4:]:
        translation_matrix.append(line.split())

    # On initialise la matrice associ�e
    matrix = [[] for x in range(int(size[1]))]
    count = 0
    iterator = 0
    # A partir de la 4�me ligne du fichier, on ajoute les �l�ments de la liste � la matrice
    for line in translation_matrix:
        for value in line:
            if count >= int(size[0]):
                count = 0
                iterator += 1
            matrix[iterator].append(value)
            count += 1
    return [matrix, magic_number, size, maximum_value]


# Fonction : Ajout d'une bordure de pixels tout autour de l'image avec une valeur de pixel de 0
# Param�tres : Matrix : matrice � modifier, filterSize : dimension en largeur du filtre
# Return : Nouvelle matrice avec bordures
def addPadding(matrix, filterSize):
    # En fonction de la taille du filtre, on ajoute le nombre n�cessaire de pixels de 0 � la matrice
    for x in range(filterSize):
        # On ajoute les lignes de pixels de 0 au d�but et � la fin de la matrice
        matrix.append(['0' for x in range(int(len(matrix[0])))])
        matrix.insert(0, ['0' for x in range(int(len(matrix[0])))])

    for line in matrix:
        for x in range(filterSize):
            # On ajoute les colonnes de pixels de 0 au d�but et � la fin de la matrice
            line.insert(0, '0')
            line.append('0')
    return matrix


# Fonction :application d'un filtre de convolution sur une matrice
# Param�tres : Matrix : la matrice sur laquelle appliquer le filtre, Filter : le filtre utilis� sur la matrice
# Return : la nouvelle matrice avec le filtre
def convolution(matrix, filter):
    # On ajoute dans un premier temps les bordures autour de l'image afin que le filtre puisse �tre appliqu� sur l'ensemble des pixels de l'image
    filterSize = int((len(filter[0]) - 1) / 2)
    newMatrix = addPadding(copy.deepcopy(matrix), filterSize)
    maxPixel = 0

    # On cr�� notre matrice sur laquelle on appliquera la convolution
    matrixConvolution = [[] for x in range(int(len(newMatrix)) - filterSize * 2)]

    for x in range(filterSize, len(newMatrix) - 1):
        for y in range(filterSize, len(newMatrix[0]) - 1):
            # On r�cup�re les valeurs des pixels voisins pour chaque pixel
            topLeft = int(newMatrix[x - 1][y - 1])
            topRight = int(newMatrix[x - 1][y + 1])
            bottomLeft = int(newMatrix[x + 1][y - 1])
            bottomRight = int(newMatrix[x + 1][y + 1])
            left = int(newMatrix[x][y - 1])
            right = int(newMatrix[x][y + 1])
            top = int(newMatrix[x - 1][y])
            bottom = int(newMatrix[x + 1][y])
            middle = int(newMatrix[x][y])

            # On applique pour chaque pixel l'op�ration de convolution par combinaison lin�aire de ses voisins
            result = int(topLeft * filter[0][0] + top * filter[0][1] + topRight * filter[0][2] + left * filter[1][0] + \
                     middle * filter[1][1] + right * filter[1][2] + bottomLeft * filter[2][0] + bottom * filter[2][1] + \
                     bottomRight * filter[2][2])
            # On applique la valeur 0 ou 255 selon si le r�sultat de l'op�ration est inf�rieur ou sup�rieur au champ des valeurs possibles
            if result < 0:
                result = 0
            elif result > 255:
                result = 255
            if result > maxPixel:
                maxPixel = result
            matrixConvolution[x - filterSize].append(result)
    return [matrixConvolution, maxPixel]


# Fonction : D�termine le gradient de l'image pour une meilleure d�tection des contours Param�tres : verticalMatrix :
# matrice associ�e � l'image avec le filtre vertical , horizontalMatrix : matrice associ�e � l'image avec le filtre
# horizontal Return : la nouvelle matrice associ�e � l'image avec d�tection de tous les contours
def outlineDetection(verticalMatrix, horizontalMatrix):
    maxPixel = 0
    outlineMatrix = [[] for x in range(int(len(verticalMatrix)))]
    for x in range(len(verticalMatrix)):
        for y in range(len(verticalMatrix[0])):
            # Approximation de la norme du gradient par combination des gradients horizontaux et verticaux (les 2 matrices)
            result = int(math.sqrt(pow(verticalMatrix[x][y], 2) + pow(horizontalMatrix[x][y], 2)))
            outlineMatrix[x].append(result)
            if result < 0:
                result = 0
            elif result > 255:
                result = 255
            if result > maxPixel:
                maxPixel = result
    return [outlineMatrix, maxPixel]


# Fonction : Applique le flou d'arri�re-plan sur l'image d'origine
# Param�tres : matrix_outline : matrice en noir et blanc avec d�tection des contours, matrix : matrice de l'image
# d'origine, matrix_blur : matrice de l'image avec flou
def blurBackground(matrix_outline, matrix, matrix_blur):
    # L'objectif est de parcourir l'image et de remplacer les valeurs des pixels de l'image d'origine par les valeurs
    # des pixels de l'image flou en parcourant l'image de diff�rentes fa�ons

    # Parcourt l'image de droite � gauche
    for x in range(0, len(matrix_outline) - 1):
        y = 0
        # Tant que le pixel est noir, on continue de remplacer les pixels de l'image d'origine par ceux de l'image flou
        while matrix_outline[x][y] == 0 and y < len(matrix_outline[0]) - 1:
            # On remplace la valeur du pixel et des 8 pixels autours
            replacePixels(matrix, matrix_blur, x, y)
            y = y + 1

    # Parcourt l'image de gauche � droite
    for x in range(0, len(matrix_outline) - 1):
        y = len(matrix_outline[0]) - 2
        # Tant que le pixel est noir, on continue de remplacer les pixels de l'image d'origine par ceux de l'image flou
        while matrix_outline[x][y] == 0 and y > 0:
            # On remplace la valeur du pixel et des 8 pixels autours
            replacePixels(matrix, matrix_blur, x, y)
            y = y - 1

    # Parcourt l'image de haut en bas
    for y in range(0, len(matrix_outline[0]) - 1):
        x = 0
        # Tant que le pixel est noir, on continue de remplacer les pixels de l'image d'origine par ceux de l'image flou
        while matrix_outline[x][y] == 0 and x < len(matrix_outline) - 1:
            # On remplace la valeur du pixel et des 8 pixels autours
            replacePixels(matrix, matrix_blur, x, y)
            x = x + 1




# Fonction : Remplace les valeurs des pixels d'une matrice par une autre matrice
# Param�tres : matrix : matrice � remplacer, matrix_blur : matrice de remplacement, x, y : positions sur la matrice
# � remplacer
def replacePixels(matrix, matrix_blur, x, y):
    matrix[x][y] = matrix_blur[x][y]
    matrix[x + 1][y + 1] = matrix_blur[x + 1][y + 1]
    matrix[x + 1][y] = matrix_blur[x + 1][y]
    matrix[x + 1][y - 1] = matrix_blur[x + 1][y - 1]
    matrix[x][y + 1] = matrix_blur[x][y + 1]
    matrix[x - 1][y + 1] = matrix_blur[x - 1][y + 1]
    matrix[x - 1][y - 1] = matrix_blur[x - 1][y - 1]
    matrix[x][y - 1] = matrix_blur[x][y - 1]
    matrix[x - 1][y] = matrix_blur[x - 1][y]


# Fonction : Seuillage de l'image
# Param�tres : Matrix : la matrice sur laquelle appliquer le seuillage
# Return : la nouvelle matrice en noir et blanc
def threshold(matrix):
    for i in range(len(matrix)):
        for y in range(len(matrix[0])):
            # On parcourt pour chaque pixel sa valeur et on affecte 0 ou 255 selon que sa valeur soit inf�rieur ou
            # sup�rieur au seuil choisi
            if int(matrix[i][y]) < 150:
                matrix[i][y] = 0
            elif int(matrix[i][y]) > 150:
                matrix[i][y] = 255


# Fonction : Ajoute du contraste � une image
# Param�tres : Matrix : la matrice sur laquelle appliquer le seuillage
# Return : la nouvelle matrice en noir et blanc
def addContrast(matrix):
    matrix_contrast = [[] for x in range(int(len(matrix)))]
    max_value = 0
    for i in range(len(matrix)):
        for y in range(len(matrix[0])):
            # Pour chaque pixel de l'image, on multiplie sa valeur par 1,5
            matrix_contrast[i].append(int(float(matrix[i][y]) * 1.5))
            # Si la valeur sort des valeurs limites possibles (inf�rieur � 0 ou sup�rieur � 255), on affecte les valeurs
            # min et max par d�faut
            if matrix_contrast[i][y] < 0:
                matrix_contrast[i][y] = 0
            elif matrix_contrast[i][y] > 255:
                matrix_contrast[i][y] = 255
            # On v�rifie si cette valeur est sup�rieure � la valeur maximale d�j� retenue, si non on la remplace
            if matrix_contrast[i][y] > max_value:
                max_value = int(matrix_contrast[i][y])
    return [matrix_contrast, max_value]


if __name__ == '__main__':

    # On commence par cr�er la matrice associ�e � l'image d'origine
    image_dataLena = createMatrix('images/lena.ascii.pgm')
    sobelFilterHorizontal = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    sobelFilterVertical = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    blur = [[0.11, 0.11, 0.11], [0.11, 0.11, 0.11], [0.11, 0.11, 0.11]]

    # On ajoute du contraste � l'image d'origine
    lenaContrast = addContrast(image_dataLena[0])

    # Cr�ation de l'image pgm de Lena avec constraste
    createImage(lenaContrast[0], "lenaContrast.pgm", image_dataLena[1],
                "image avec contraste", image_dataLena[2][0], image_dataLena[2][1], lenaContrast[1])

    # On ajoute du flou � l'image d'origine
    lenaBlur = convolution(image_dataLena[0], blur)

    for i in range(30):
        lenaBlur = convolution(lenaBlur[0], blur)

    # Cr�ation de l'image pgm de Lena avec flou
    createImage(lenaBlur[0], "lenaBlur.pgm", image_dataLena[1],
                "image avec flou", image_dataLena[2][0], image_dataLena[2][1], lenaBlur[1])

    # Application du filtre de Sobel sur l'image d'origine
    verticalLenaImageSobelConvolution = convolution(lenaContrast[0], sobelFilterVertical)
    horizontalLenaImageSobelConvolution = convolution(lenaContrast[0], sobelFilterHorizontal)

    lenaImageSobelOutlineDetection = outlineDetection(verticalLenaImageSobelConvolution[0],
                                                      horizontalLenaImageSobelConvolution[0])

    # Seuillage de l'image
    threshold(lenaImageSobelOutlineDetection[0])

    # Cr�ation de l'image pgm de Lena avec d�tection des contours en noir et blanc
    createImage(lenaImageSobelOutlineDetection[0], "lenaImageSobelOutlineDetection.pgm", image_dataLena[1],
                "image avec d�tection des contours", image_dataLena[2][0],
                image_dataLena[2][1], lenaImageSobelOutlineDetection[1])

    # Application du flou d'arri�re-plan sur l'image d'origine
    blurBackground(lenaImageSobelOutlineDetection[0], image_dataLena[0],
                   lenaBlur[0])

    # Cr�ation de l'image pgm de Lena avec flou d'arri�re plan
    createImage(image_dataLena[0], "lenaImageblurBackground.pgm", image_dataLena[1],
                "image avec flou d'arri�re plan", image_dataLena[2][0], image_dataLena[2][1], image_dataLena[3])
