import math
import sys


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


# Fonction : Pivotement d'une matrice à 180°
# Paramètres : matrix = matrice à pivoter
# Return : matrice inversée
def invertMatrix(matrix):
    # On effectue une copie de la matrice à inverser
    inverted_matrix = matrix.copy()
    # On inverse l'ordre de chaque ligne puis on inverse l'ordre de chaque colonne
    for line in inverted_matrix:
        line.reverse()
    inverted_matrix.reverse()
    return inverted_matrix


# Fonction : Création d'une nouvelle image
# Paramètres : matrix = matrice à ajouter, magic_number = nombre magique de l'image,
#           comments = commentaires sur l'image, width = largeur de l'image, height = hauteur de l'image,
#           maximum_value = intensité maximale
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

# Fonction : Convertir un fichier pgm en pbm
# Paramètres : matrix = matrice à ajouter, size = dimensions de l'image, maximum_value = intensité maximale
# Return : Matrice binaire
def createPBM(matrix, size, maximum_value):
    newMaxValue = math.floor(int(maximum_value) / 2)
    convertMatrix = [[] for x in range(int(size))]
    for i, line in enumerate(matrix):
        for j, value in enumerate(line):
            # Convertit les valeurs de la matrice en 1 si supérieur à la moitié de l'intensité maximale
            if int(value) > newMaxValue:
                convertMatrix[i].append(1)
            # Convertit les valeurs de la matrice en 0 si inférieur à la moitié de l'intensité maximale
            else:
                convertMatrix[i].append(0)
    return convertMatrix


# Fonction : Réduction d'une matrice par 2
# Paramètres : matrix = matrice à réduire
# Return : matrice réduite
def reduceMatrix(matrix):
    # On créé la matrice qui contiendra la matrice réduite
    reduced_matrix = []
    for i in range(0, len(matrix), 2):
        line = []
        for j in range(0, len(matrix[1]), 2):
            # On stocke la valeur de chaque pixel qui correspond à la moyenne du pixel correspondant et des 3 pixels qui l'entourent
            if i == len(matrix) - 1:  # Cas où le pixel est sur la dernière ligne
                if j == len(matrix[1]) - 1:  # Cas où le pixel est sur la dernière ligne et dernière colonne
                    value = int(matrix[i][j])
                else:
                    value = (int(matrix[i][j]) + int(matrix[i][j + 1])) / 4
            elif j == len(matrix[1]) - 1:  # Cas où le pixel est sur la dernière colonne
                value = (int(matrix[i][j]) + int(matrix[i + 1][j])) / 4
            else:
                value = (int(matrix[i][j]) + int(matrix[i + 1][j]) + int(matrix[i][j + 1]) + int(
                    matrix[i + 1][j + 1])) / 4
            line.append(int(value))
        reduced_matrix.append(line)
    return reduced_matrix


def main():
    # Question 5
    image_data = createMatrix('images/feep.ascii.pgm')
    image_data2 = createMatrix('images/lena.ascii.pgm')

    # Question 6
    createImage(image_data[0], "matrixCopy.pgm", image_data[1], "copy of the matrix", image_data[2][0],
                image_data[2][1],
                image_data[3])
    createImage(image_data2[0], "matrixCopy2.pgm", image_data2[1], "copy of the matrix", image_data2[2][0],
                image_data2[2][1],
                image_data2[3])

    # Question 7
    inverted_matrix = invertMatrix(image_data[0])
    createImage(inverted_matrix, "invertedMatrix.pgm", image_data[1], "inversion of the matrix", image_data[2][0],
                image_data[2][1], image_data[3])
    inverted_matrix2 = invertMatrix(image_data2[0])
    createImage(inverted_matrix2, "invertedMatrix2.pgm", image_data2[1], "inversion of the matrix", image_data2[2][0],
                image_data2[2][1], image_data2[3])

    # Question 8
    bpm_matrix = createPBM(image_data[0], image_data[2][1], image_data[3])
    createImage(bpm_matrix, "pbmMatrix.pbm", "P1", "convert pgm file to pbm", image_data[2][0],
                image_data[2][1], 0)
    bpm_matrix2 = createPBM(image_data2[0], image_data2[2][1], image_data2[3])
    createImage(bpm_matrix2, "pbmMatrix2.pbm", "P1", "convert pgm file to pbm", image_data2[2][0],
                image_data2[2][1], 0)

    # Question 9
    reduced_matrix = reduceMatrix(image_data[0])
    createImage(reduced_matrix, "reducedImage.pgm", image_data[1], "image reduced by 2", len(reduced_matrix[1]),
                len(reduced_matrix), image_data[3])
    reduced_matrix2 = reduceMatrix(image_data2[0])
    createImage(reduced_matrix2, "reducedImage2.pgm", image_data2[1], "image reduced by 2", len(reduced_matrix2[1]),
                len(reduced_matrix2), image_data2[3])


if __name__ == '__main__':
    sys.exit(main())
