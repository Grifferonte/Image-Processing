import copy
import math

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

    # On créé une liste provisoire qui contient l'ensemble des valeurs des pixels à la suite
    translation_matrix = []
    for line in lines[4:]:
        translation_matrix.append(line.split())

    # On initialise la matrice associée
    matrix = [[] for x in range(int(size[1]))]
    count = 0
    iterator = 0
    # A partir de la 4ème ligne du fichier, on ajoute les éléments de la liste à la matrice
    for line in translation_matrix:
        for value in line:
            if count >= int(size[0]):
                count = 0
                iterator += 1
            matrix[iterator].append(value)
            count += 1
    return [matrix, magic_number, size, maximum_value]


# Fonction : Ajout d'une bordure de pixels tout autour de l'image avec une valeur de pixel de 0
# Paramètres : Matrix : matrice à modifier, filterSize : dimension en largeur du filtre
# Return : Nouvelle matrice avec bordures
def addPadding(matrix, filterSize):
    # En fonction de la taille du filtre, on ajoute le nombre nécessaire de pixels de 0 à la matrice
    for x in range(filterSize):
        # On ajoute les lignes de pixels de 0 au début et à la fin de la matrice
        matrix.append(['0' for x in range(int(len(matrix[0])))])
        matrix.insert(0, ['0' for x in range(int(len(matrix[0])))])

    for line in matrix:
        for x in range(filterSize):
            # On ajoute les colonnes de pixels de 0 au début et à la fin de la matrice
            line.insert(0, '0')
            line.append('0')
    return matrix


# Fonction :application d'un filtre de convolution sur une matrice
# Paramètres : Matrix : la matrice sur laquelle appliquer le filtre, Filter : le filtre utilisé sur la matrice
# Return : la nouvelle matrice avec le filtre
def convolution(matrix, filter):
    # On ajoute dans un premier temps les bordures autour de l'image afin que le filtre puisse être appliqué sur l'ensemble des pixels de l'image
    filterSize = int((len(filter[0]) - 1) / 2)
    newMatrix = addPadding(copy.deepcopy(matrix), filterSize)
    maxPixel = 0

    # On créé notre matrice sur laquelle on appliquera la convolution
    matrixConvolution = [[] for x in range(int(len(newMatrix)) - filterSize * 2)]

    for x in range(filterSize, len(newMatrix) - 1):
        for y in range(filterSize, len(newMatrix[0]) - 1):
            # On récupère les valeurs des pixels voisins pour chaque pixel
            topLeft = int(newMatrix[x - 1][y - 1])
            topRight = int(newMatrix[x - 1][y + 1])
            bottomLeft = int(newMatrix[x + 1][y - 1])
            bottomRight = int(newMatrix[x + 1][y + 1])
            left = int(newMatrix[x][y - 1])
            right = int(newMatrix[x][y + 1])
            top = int(newMatrix[x - 1][y])
            bottom = int(newMatrix[x + 1][y])
            middle = int(newMatrix[x][y])

            # On applique pour chaque pixel l'opération de convolution par combinaison linéaire de ses voisins
            result = topLeft * filter[0][0] + top * filter[0][1] + topRight * filter[0][2] + left * filter[1][0] + \
                     middle * filter[1][1] + right * filter[1][2] + bottomLeft * filter[2][0] + bottom * filter[2][1] + \
                     bottomRight * filter[2][2]
            #On applique la valeur 0 ou 255 selon si le résultat de l'opération est inférieur ou supérieur au champ des valeurs possibles
            if result > maxPixel:
                maxPixel = result
            if (result < 0):
                result = 0
            matrixConvolution[x - filterSize].append(result)
    return [matrixConvolution, maxPixel]

# Fonction : Détermine le gradient de l'image pour une meilleure détection des contours
# Paramètres : verticalMatrix : matrice associée à l'image avec le filtre vertical , horizontalMatrix : matrice associée à l'image avec le filtre horizontal
# Return : la nouvelle matrice associée à l'image avec détection de tous les contours
def outlineDetection(verticalMatrix, horizontalMatrix):
    maxPixel = 0
    outlineMatrix = [[] for x in range(int(len(verticalMatrix)))]
    for x in range(len(verticalMatrix)):
        for y in range(len(verticalMatrix[0])):
             # Approximation de la norme du gradient par combination des gradients horizontaux et verticaux (les 2 matrices)
            result = int(math.sqrt(pow(verticalMatrix[x][y], 2) + pow(horizontalMatrix[x][y], 2)))
            outlineMatrix[x].append(result)
            if result > maxPixel:
                maxPixel = result
    return [outlineMatrix, maxPixel]

if __name__ == '__main__':
    # Question 1 :
    image_dataFeep = createMatrix('images/feep.ascii.pgm')
    image_dataLena = createMatrix('images/lena.ascii.pgm')
    prewittFilterHorizontal = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    prewittFilterVertical = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
    sobelFilterHorizontal = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    sobelFilterVertical = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    verticalFeepImagePrewittConvolution = convolution(image_dataFeep[0], prewittFilterVertical)
    horizontalFeepImagePrewittConvolution = convolution(image_dataFeep[0], prewittFilterHorizontal)
    verticalLenaImagePrewittConvolution = convolution(image_dataLena[0], prewittFilterVertical)
    horizontalLenaImagePrewittConvolution = convolution(image_dataLena[0], prewittFilterHorizontal)

    verticalFeepImageSobelConvolution = convolution(image_dataFeep[0], sobelFilterVertical)
    horizontalFeepImageSobelConvolution = convolution(image_dataFeep[0], sobelFilterHorizontal)
    verticalLenaImageSobelConvolution = convolution(image_dataLena[0], sobelFilterVertical)
    horizontalLenaImageSobelConvolution = convolution(image_dataLena[0], sobelFilterHorizontal)

    # Question 2 :
    createImage(verticalFeepImagePrewittConvolution[0], "verticalFeepImagePrewittConvolution.pgm", image_dataFeep[1],
                "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], verticalFeepImagePrewittConvolution[1])
    createImage(horizontalFeepImagePrewittConvolution[0], "horizontalFeepImagePrewittConvolution.pgm",
                image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], horizontalFeepImagePrewittConvolution[1])
    createImage(verticalLenaImagePrewittConvolution[0], "verticalLenaImagePrewittConvolution.pgm", image_dataLena[1],
                "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], verticalLenaImagePrewittConvolution[1])
    createImage(horizontalLenaImagePrewittConvolution[0], "horizontalLenaImagePrewittConvolution.pgm",
                image_dataLena[1],
                "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], horizontalLenaImagePrewittConvolution[1])

    createImage(verticalFeepImageSobelConvolution[0], "verticalFeepImageSobelConvolution.pgm", image_dataFeep[1],
                "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], verticalFeepImageSobelConvolution[1])
    createImage(horizontalFeepImageSobelConvolution[0], "horizontalFeepImageSobelConvolution.pgm", image_dataFeep[1],
                "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], horizontalFeepImageSobelConvolution[1])
    createImage(verticalLenaImageSobelConvolution[0], "verticalLenaImageSobelConvolution.pgm", image_dataLena[1],
                "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], verticalLenaImageSobelConvolution[1])
    createImage(horizontalLenaImageSobelConvolution[0], "horizontalLenaImageSobelConvolution.pgm", image_dataLena[1],
                "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], horizontalLenaImageSobelConvolution[1])

    # Question 3 :
    feepImagePrewittOutlineDetection = outlineDetection(verticalFeepImagePrewittConvolution[0],
                                                        horizontalFeepImagePrewittConvolution[0])
    lenaImagePrewittOutlineDetection = outlineDetection(verticalLenaImagePrewittConvolution[0],
                                                        horizontalLenaImagePrewittConvolution[0])
    feepImageSobelOutlineDetection = outlineDetection(verticalFeepImageSobelConvolution[0],
                                                      horizontalFeepImageSobelConvolution[0])
    lenaImageSobelOutlineDetection = outlineDetection(verticalLenaImageSobelConvolution[0],
                                                      horizontalLenaImageSobelConvolution[0])

    createImage(feepImagePrewittOutlineDetection[0], "feepImagePrewittOutlineDetection.pgm", image_dataFeep[1],
                "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], feepImagePrewittOutlineDetection[1])
    createImage(lenaImagePrewittOutlineDetection[0], "lenaImagePrewittOutlineDetection.pgm", image_dataLena[1],
                "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], lenaImagePrewittOutlineDetection[1])
    createImage(feepImageSobelOutlineDetection[0], "feepImageSobelOutlineDetection.pgm", image_dataFeep[1],
                "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], feepImageSobelOutlineDetection[1])
    createImage(lenaImageSobelOutlineDetection[0], "lenaImageSobelOutlineDetection.pgm", image_dataLena[1],
                "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], lenaImageSobelOutlineDetection[1])