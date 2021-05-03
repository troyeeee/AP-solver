import sys
from pprint import pprint
import assignment_problem_min as apm
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from munkres import Munkres, print_matrix
import subprocess

ui, _ = loadUiType('Hungarian.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

    def Handle_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.solutionOutput.setReadOnly(True)
        self.answerOutput.setReadOnly(True)
        self.solutionOutput_2.setReadOnly(True)
        self.answerOutput.setReadOnly(True)

    def Handle_Buttons(self):
        self.configureAssignmentButton.clicked.connect(self.Handle_Matrices)
        self.refreshButton.clicked.connect(self.RefreshAction)
        self.backButton.clicked.connect(self.BackAction)
        self.playButton.clicked.connect(self.PlayAction)
        self.modifyButton.clicked.connect(self.ModifyButton)
        self.homeButton.clicked.connect(self.HomeButton)
        self.refreshButton_2.clicked.connect(self.RefreshAction_Max)
        self.backButton_2.clicked.connect(self.BackAction_Max)
        self.playButton_2.clicked.connect(self.PlayAction_Max)
        self.modifyButton_2.clicked.connect(self.ModifyButton_Max)
        self.homeButton_2.clicked.connect(self.HomeButton_Max)

    def Handle_Matrices(self):
        temp = self.hungarianChooser.currentText()
        if temp == 'Minimization':
            self.CreateMatrix()
        else:
            self.CreateMatrix_Max()

    # =----------------------------------------------------------------------MAXIMIZATION------------------------------------------------------#
    # ------------------------------------------------------------------------------------------------------------------------------------------#
    def CreateMatrix_Max(self):
        row_number = int(self.rowNumber.currentText()) + 1
        column_number = int(self.columnNumber.currentText()) + 1

        self.matrixTable_2.setRowCount(row_number)
        self.matrixTable_2.setColumnCount(column_number)

        for i in range(1, row_number):
            for j in range(1, column_number):
                self.matrixTable_2.setItem(i, j, QTableWidgetItem('0'))

        for i in range(1, column_number):
            self.matrixTable_2.setItem(0, i, QTableWidgetItem('job ' + str(i)))

        for i in range(1, row_number):
            self.matrixTable_2.setItem(i, 0, QTableWidgetItem('name ' + str(i)))

        self.tabWidget.setCurrentIndex(3)

    def RefreshAction_Max(self):
        self.CreateMatrix_Max()

    def BackAction_Max(self):
        self.tabWidget.setCurrentIndex(0)
        self.rowNumber.setCurrentIndex(0)
        self.columnNumber.setCurrentIndex(0)

    def PlayAction_Max(self):
        print("PlayAction po")
        self.AssignmentProblemMax()
        self.tabWidget.setCurrentIndex(4)

    def HomeButton_Max(self):
        self.tabWidget.setCurrentIndex(0)

    def ModifyButton_Max(self):
        self.tabWidget.setCurrentIndex(3)

    def AssignmentProblemMax(self):
        print('Hello Po')
        arr = []
        numberOfRows = int(self.rowNumber.currentText())
        numberOfColumns = int(self.columnNumber.currentText())

        for i in range(1, numberOfRows + 1):
            for j in range(1, numberOfColumns + 1):
                arr.append(int(self.matrixTable_2.item(i, j).text()))

        stringRows = []
        stringCol = []

        for i in range(1, numberOfRows + 1):
            stringRows.append(self.matrixTable_2.item(i, 0).text())

        for i in range(1, numberOfColumns + 1):
            stringCol.append(self.matrixTable_2.item(0, i).text())

        np_arr = np.array(arr)
        np_arr = np_arr.reshape(numberOfRows, numberOfColumns)

        np_arr_2 = np.array(arr)
        np_arr_2 = np_arr_2.reshape(numberOfRows,numberOfColumns)

        #########################The Solution##############################

        theSolution = "THE SOLUTION : \n"
        # Creating Temporary array of zeros
        temp_arr = np.zeros(numberOfRows * numberOfColumns, dtype=int)
        temp_arr = temp_arr.reshape(numberOfRows, numberOfColumns)
        #
        temp_arr_2 = np.zeros(numberOfRows * numberOfColumns, dtype=int)
        temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns)
        np.place(temp_arr_2, temp_arr_2 == 0, 1)

        temp_arr = np.invert(np_arr_2) + temp_arr_2

        theSolution += "Negate all values : \n"
        theSolution += "Because the objective is to maximize the total cost we negate all elements:\n"
        theSolution += str(temp_arr) + '\n'
        theSolution += '\n'

        temp_arr_2 = np.zeros(numberOfRows * numberOfColumns, dtype=int)
        temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns)

        theSolution += "Make the Matrix non negative\n"
        theSolution += "we add the maximum value to each entry to make the cost matrix non negative:\n"
        maxNumber = np.amax(np_arr_2)

        for i in range(0, numberOfColumns):
            temp_arr_2[:, i] = maxNumber

        temp_arr = temp_arr + temp_arr_2
        theSolution += str(temp_arr) + '\n'

        theSolution += '\n'
        theSolution += "Subtract Minimum Row Values\n"

        temp_arr_2 = np.zeros(numberOfRows * numberOfColumns, dtype=int)
        temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns)

        row_minima = np.amin(temp_arr, axis=1)

        for i in range(0, len(row_minima)):
            temp_arr_2[i, :] = row_minima[i]

        temp_arr = temp_arr - temp_arr_2
        theSolution += str(temp_arr) + '\n'

        theSolution += '\n'
        theSolution += "Subtract Minimum Column Values" + '\n'

        temp_arr_2 = np.zeros(numberOfRows * numberOfColumns, dtype=int)
        temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns)

        col_minima = np.amin(temp_arr, axis=0)

        for i in range(0, len(col_minima)):
            temp_arr_2[:, i] = col_minima[i]

        temp_arr = temp_arr - temp_arr_2
        theSolution += str(temp_arr) + '\n'
        theSolution += "\nCover all zeros with a minimum number of lines\n"
        theSolution += "Create Additional zeros\n"




        ###################################################################
        matrix = np_arr

        cost_matrix = []
        for row in matrix:
            cost_row = []
            for col in row:
                cost_row += [sys.maxsize - col]
            cost_matrix += [cost_row]

        m = Munkres()
        indexes = m.compute(cost_matrix)
        theOriginalMatrix = 'THE ORIGINAL MATRIX\n'
        theOriginalMatrix += str(matrix) + '\n'
        theOriginalMatrix += '\n'
        theFinalAnswer = 'Highest profit through this matrix:\n'
        theFinalAnswer += str(matrix) + '\n'
        theFinalAnswer += '\n'
        total = 0

        theFinalAnswer += 'Index of Each Row and Column in the Matrix\n'
        for row, column in indexes:
            value = matrix[row][column]
            total += value
            theFinalAnswer += ('(%d, %d) -> %d' % (row, column, value))
            theFinalAnswer += '\n'

        theFinalAnswer += '\nAssigned Values: \n'
        for row, column in indexes:
            theFinalAnswer += stringRows[row] + ' is assigned to ' + stringCol[column]
            theFinalAnswer += '\n'

        theFinalAnswer += '\n'
        theFinalAnswer += ('total profit=%d' % total)

        self.answerOutput_2.setText(theFinalAnswer)

        self.solutionOutput_2.setText(theOriginalMatrix + '\n' + theSolution +'\n' + theFinalAnswer)




    # =----------------------------------------------------------------------MINIMIZATION------------------------------------------------------#
    # ------------------------------------------------------------------------------------------------------------------------------------------#
    def CreateMatrix(self):
        outfile = open("data.jnfljc", "w")
        outfile.write("")
        outfile.close()

        row_number = int(self.rowNumber.currentText()) + 1
        column_number = int(self.columnNumber.currentText()) + 1

        self.matrixTable.setRowCount(row_number)
        self.matrixTable.setColumnCount(column_number)

        for i in range(1, row_number):
            for j in range(1, column_number):
                self.matrixTable.setItem(i, j, QTableWidgetItem('0'))

        for i in range(1, column_number):
            self.matrixTable.setItem(0, i, QTableWidgetItem('job ' + str(i)))

        for i in range(1, row_number):
            self.matrixTable.setItem(i, 0, QTableWidgetItem('name ' + str(i)))

        self.tabWidget.setCurrentIndex(1)

    def RefreshAction(self):
        self.CreateMatrix()

    def BackAction(self):
        self.tabWidget.setCurrentIndex(0)
        self.rowNumber.setCurrentIndex(0)
        self.columnNumber.setCurrentIndex(0)

    def PlayAction(self):
        self.tabWidget.setCurrentIndex(2)
        self.AssignmentProblemMin()

    def HomeButton(self):
        self.tabWidget.setCurrentIndex(0)

    def ModifyButton(self):
        outfile = open("data.jnfljc", "w")
        outfile.write("")
        outfile.close()
        self.tabWidget.setCurrentIndex(1)

    def AssignmentProblemMin(self):
        arr = []
        numberOfRows = int(self.rowNumber.currentText())
        numberOfColumns = int(self.columnNumber.currentText())

        for i in range(1, numberOfRows + 1):
            for j in range(1, numberOfColumns + 1):
                arr.append(int(self.matrixTable.item(i, j).text()))

        np_arr = np.array(arr)
        np_arr = np_arr.reshape(numberOfRows, numberOfColumns)

        np_arr2 = np.array(arr)
        np_arr2 = np_arr2.reshape(numberOfRows, numberOfColumns)

        theOriginalMatrix = ''
        theOriginalMatrix += 'THE ORIGINAL MATRIX\n'
        theOriginalMatrix += str(np_arr)
        theOriginalMatrix += '\n'

        stringRows = []
        stringCol = []

        for i in range(1, numberOfRows + 1):
            stringRows.append(self.matrixTable.item(i, 0).text())

        for i in range(1, numberOfColumns + 1):
            stringCol.append(self.matrixTable.item(0, i).text())

        theSolution = "\nTHE SOLUTION\n"

        if (numberOfRows > numberOfColumns):
            temp_arr = np_arr2
            theSolution += '\n'
            theSolution += "Subtract Minimum Row Values\n"

            temp_arr_2 = np.zeros(numberOfRows * numberOfColumns, dtype=int)
            temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns)

            row_minima = np.amin(temp_arr, axis=1)

            for i in range(0, len(row_minima)):
                temp_arr_2[i, :] = row_minima[i]

            temp_arr = temp_arr - temp_arr_2
            theSolution += str(temp_arr) + '\n'

            theSolution += '\n'
            theSolution += "Subtract Minimum Column Values" + '\n'

            temp_arr_2 = np.zeros(numberOfRows * numberOfColumns, dtype=int)
            temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns)

            col_minima = np.amin(temp_arr, axis=0)

            for i in range(0, len(col_minima)):
                temp_arr_2[:, i] = col_minima[i]

            temp_arr = temp_arr - temp_arr_2
            theSolution += str(temp_arr) + '\n'
            theSolution += "\nCover all zeros with a minimum number of lines\n"
            theSolution += "Create Additional zeros\n"
        else:
            tempText = apm.hungarianMethod(np_arr)

        from scipy.optimize import linear_sum_assignment
        row_ind, col_ind = linear_sum_assignment(np_arr)

        theFinalAnswer = ''

        theFinalAnswer += "The Original Array is : \n"
        theFinalAnswer += str(np_arr2) + '\n'
        theFinalAnswer += "\nIndex of each row and column in the matrix and value\n"
        for i in range(0, len(row_ind)):
            theFinalAnswer += '(' + str(row_ind[i]) + ', ' + str(col_ind[i]) + ')' + ' --> ' + str(
                np_arr2[row_ind[i]][col_ind[i]]) + '\n'
        theFinalAnswer += '\n'

        theFinalAnswer += 'Assigned Values: \n'

        optimal_value = 0

        for i in range(0, len(row_ind)):
            theFinalAnswer += stringRows[row_ind[i]] + ' is assigned to ' + stringCol[col_ind[i]] + '\n'
            optimal_value += int(np_arr2[row_ind[i]][col_ind[i]])
        # print(str(row_ind[i]) + ' ' + str(col_ind[i]))
        # print(np_arr2)
        # print(optimal_value)

        theFinalAnswer += '\n' + 'The Optimal Value is: ' + str(optimal_value)

        # the solution from our data.jnfljc
        theSolutionArr = []
        with open("data.jnfljc") as file:
            for line in file:
                line = line.replace("\n", "")
                theSolutionArr.append(line)



        for i in theSolutionArr:
            theSolution += i + '\n'

        theSolution += '\n'
        theWholeText = ''
        theWholeText += theOriginalMatrix
        theWholeText += theSolution
        theWholeText += theFinalAnswer

        self.solutionOutput.setText(theWholeText)
        self.answerOutput.setText(theFinalAnswer)


################################################################################################################################################


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
