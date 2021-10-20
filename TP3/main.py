import math

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

def addPadding(matrix, filterSize):
    for x in range(filterSize):
        matrix.append(['0' for x in range(int(len(matrix[0])))])
        matrix.insert(0,['0' for x in range(int(len(matrix[0])))])

    for line in matrix:
        for x in range(filterSize):
            line.insert(0,'0')
            line.append('0')
    return matrix

def convolution(matrix, filter):
    filterSize = int((len(filter[0])-1) / 2)
    newMatrix = addPadding(matrix, filterSize)

    matrixConvolution = [[] for x in range(int(len(newMatrix)) - filterSize * 2)]

    for x in range(filterSize, len(newMatrix) - 1):
        for y in range(filterSize,len(newMatrix[0])-1):

            topLeft = int(newMatrix[x-1][y-1])
            topRight = int(newMatrix[x-1][y+1])
            bottomLeft = int(newMatrix[x+1][y-1])
            bottomRight = int(newMatrix[x+1][y+1])
            left = int(newMatrix[x][y-1])
            right = int(newMatrix[x][y+1])
            top = int(newMatrix[x-1][y])
            bottom = int(newMatrix[x+1][y])
            middle = int(matrix [x][y])

            result = topLeft * filter[0][0] + top * filter[0][1] + topRight * filter[0][2] + left * filter[1][0] + middle * filter[1][1] + right * filter[1][2] + bottomLeft * filter[2][0] + bottom * filter[2][1] + bottomRight * filter[2][2]
            if (result < 0):
                result = 0
            matrixConvolution[x - filterSize].append(result)
    return matrixConvolution

def outlineDetection(verticalMatrix, horizontalMatrix):
    outlineMatrix = [[] for x in range(int(len(verticalMatrix)))]
    for x in range(len(verticalMatrix)):
        for y in range(len(verticalMatrix[0])):
            outlineMatrix[x].append(int(math.sqrt(pow(verticalMatrix[x][y],2) + pow(horizontalMatrix[x][y],2))))
    return outlineMatrix

def createImage(matrix, file_name, magic_number, comments, width, height, maximum_value):
    fic = open(file_name, 'w')  # On ouvre le fichier PGM en écriture
    fic.write(magic_number + '\n')  # On note le format du fichier
    fic.write('# ' + comments + '\n')  # Commentaires facultatifs
    fic.write(str(width) + ' ' + str(height) + '\n')  # On note ses dimensions
    if maximum_value!=0:
        fic.write(str(maximum_value) + '\n')  # On note la valeur de l'intensité maximale
    # On note les valeurs de la matrice
    for line in matrix:
        for value in line:
            fic.write(str(value) + ' ')
        fic.write('\n')
    fic.write('\n')
    fic.close()


if __name__ == '__main__':
    # Question 1 :
    image_dataFeep = createMatrix('images/feep.ascii.pgm')
    image_dataLena = createMatrix('images/lena.ascii.pgm')
    prewittFilterHorizontal = [[1,0,-1],[1,0,-1],[1,0,-1]]
    prewittFilterVertical = [[1,1,1],[0,0,0],[-1,-1,-1]]
    sobelFilterHorizontal = [[1,0,-1],[2,0,-2],[1,0,-1]]
    sobelFilterVertical = [[1,2,1],[0,0,0],[-1,-2,-1]]

    verticalFeepImagePrewittConvolution = convolution(image_dataFeep[0], prewittFilterVertical)
    horizontalFeepImagePrewittConvolution = convolution(image_dataFeep[0], prewittFilterHorizontal)
    verticalLenaImagePrewittConvolution = convolution(image_dataLena[0], prewittFilterVertical)
    horizontalLenaImagePrewittConvolution = convolution(image_dataLena[0], prewittFilterHorizontal)

    verticalFeepImageSobelConvolution = convolution(image_dataFeep[0], sobelFilterVertical)
    horizontalFeepImageSobelConvolution = convolution(image_dataFeep[0], sobelFilterHorizontal)
    verticalLenaImageSobelConvolution = convolution(image_dataLena[0], sobelFilterVertical)
    horizontalLenaImageSobelConvolution = convolution(image_dataLena[0], sobelFilterHorizontal)

    # Question 2 :
    createImage(verticalFeepImagePrewittConvolution, "verticalFeepImagePrewittConvolution.pgm", image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], image_dataFeep[3])
    createImage(horizontalFeepImagePrewittConvolution, "horizontalFeepImagePrewittConvolution.pgm", image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], image_dataFeep[3])
    createImage(verticalLenaImagePrewittConvolution, "verticalLenaImagePrewittConvolution.pgm", image_dataLena[1], "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], image_dataLena[3])
    createImage(horizontalLenaImagePrewittConvolution, "horizontalLenaImagePrewittConvolution.pgm", image_dataLena[1], "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], image_dataLena[3])

    createImage(verticalFeepImageSobelConvolution, "verticalFeepImageSobelConvolution.pgm", image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], image_dataFeep[3])
    createImage(horizontalFeepImageSobelConvolution, "horizontalFeepImageSobelConvolution.pgm", image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], image_dataFeep[3])
    createImage(verticalLenaImageSobelConvolution, "verticalLenaImageSobelConvolution.pgm", image_dataLena[1], "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], image_dataLena[3])
    createImage(horizontalLenaImageSobelConvolution, "horizontalLenaImageSobelConvolution.pgm", image_dataLena[1], "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], image_dataLena[3])



    #Question 3 :
    feepImagePrewittOutlineDetection = outlineDetection(verticalFeepImagePrewittConvolution, horizontalFeepImagePrewittConvolution)
    lenaImagePrewittOutlineDetection = outlineDetection(verticalLenaImagePrewittConvolution, horizontalLenaImagePrewittConvolution)
    feepImageSobelOutlineDetection = outlineDetection(verticalFeepImageSobelConvolution, horizontalFeepImageSobelConvolution)
    lenaImageSobelOutlineDetection = outlineDetection(verticalLenaImageSobelConvolution, horizontalLenaImageSobelConvolution)

    createImage(feepImagePrewittOutlineDetection, "feepImagePrewittOutlineDetection.pgm", image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], image_dataFeep[3])
    createImage(lenaImagePrewittOutlineDetection, "lenaImagePrewittOutlineDetection.pgm", image_dataFeep[1], "inversion of the matrix", image_dataFeep[2][0],
                image_dataFeep[2][1], image_dataFeep[3])
    createImage(feepImageSobelOutlineDetection, "feepImageSobelOutlineDetection.pgm", image_dataLena[1], "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], image_dataLena[3])
    createImage(lenaImageSobelOutlineDetection, "lenaImageSobelOutlineDetection.pgm", image_dataLena[1], "inversion of the matrix", image_dataLena[2][0],
                image_dataLena[2][1], image_dataLena[3])