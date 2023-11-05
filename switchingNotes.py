import fitz
import os
import shutil 
import re

basePath = "//mnt//e//pyProj//booksProj"
src = basePath + '//OG.pdf'
edit = basePath + '//OG.pdf'


fstPgAdded = 0
lstPgAdded = 132




def updatePDF(initReplace, finReplace, ogPath, toBeEditiedPath):

    """
    Description: This function takes two pdf paths as input and replace a set of pages in the toBeEditied one with
    A bunch of pages from the og one

    initReplace: An int that indicates the starting page. Numbering is zero-based. Inclusive
    finReplace: An int that indicates the final page. Numbering is zero-based. Inclusive
    ogPath: Path of the pdf to grab from. A string
    toBeEditedPath: Path of the pdf to edit and update. A string
    """

    #open docs.
    doc = fitz.open(ogPath)
    doc_cop = fitz.open(toBeEditiedPath)

    #remove the pages that are to be updated
    doc_cop.delete_pages(fstPgAdded,lstPgAdded)
    #replace those pages with newer versions from a different pdf.
    doc_cop.insert_pdf(doc, from_page = initReplace, to_page = finReplace, start_at = initReplace)

    #save the document. Need to save it to a new file first since garbage can't
    #be done with incremental saving.
    doc_cop.save('55.pdf', garbage = 4, deflate = True)
    #os.remove(edit)

    #make that new file become the old file afterwards
    shutil.move('55.pdf', edit)
    doc_cop.close()
    doc.close()




def displayAnnots(pdfPath, pageRange):

    """
    Desription: prints all the annotations within a certain range to the terminal
    pdfPath: A string that contains the path to the pdf
    page_range: number of page from the top of the documents to scan

    """

    #open doc
    doc = fitz.open(pdfPath)

    #loop through each page within specified range
    for i in range(pageRange):
        #get annotations holder for each page
        page_annots = doc[i].annots()
        for annot in page_annots:
            #print each annotation
            print(i + 1, annot.info)

    doc.close()





def getAnnotatedPages(pdfPath, fstPgToScan, lstPgToScan):

    """
    Desription: prints all the annotations within a certain range to the terminal. Numbering is zero based and inclusive
    pdfPath: A string that contains the path to the pdf
    page_range: number of page from the top of the documents to scan

    """
    with open('indecies.txt', 'w') as f:
        #open doc
        doc = fitz.open(pdfPath)

        #loop through each page within specified range
        for i in range(fstPgToScan, lstPgToScan + 1):
            

            #get annotations holder for each page
            if doc[i].annot_xrefs() != []:
                f.write(str(i) + ', ')
                doc2 = fitz.open()
                doc2.insert_pdf(doc, i,i)
                doc2.save("pages/Page{0:04d}.pdf".format(i))
                doc2.close()
                

        doc.close()





def joinAndIndex(filesPath):


    files = os.listdir(filesPath)
    print(files)
    totalFile = fitz.open()
    for file in files:
        print(file)
        doc = fitz.open(basePath + '//pages//' + file)
        totalFile.insert_pdf(doc, 0, 0)
        doc.close()
    
    totalFile.save("total.pdf", garbage = 4, deflate = True)


def parseTxt(txtFilePath):

    """
    Description: Parses a text file into a list of indecies that indicate the original
    Position the pages held in the original file

    txtFilePath: a string that holds the absolute position of the text file

    Returns: A list of indecies

    """
    indecies_list = []
    with open(txtFilePath, 'r') as f:

        content = f.read()
    
    pat = re.findall('[0-9]*, ', content)
    for num in pat:
        indecies_list.append(int(num[:-2]))

    return indecies_list


def reinstate(rplcmntPDFPath, toBeEditedPDFPath, indecies_list):


    """
    Description: Swaps out older versions of pages 

    """
    rplcmnt = fitz.open(rplcmntPDFPath)
    edit = fitz.open(toBeEditedPDFPath)
    i = 0
    for index in indecies_list:
        
        edit.insert_pdf(rplcmnt, from_page = i, to_page = i, start_at = index)
        edit.delete_page(index + 1)
        
        print(index)
        print(i)


        i += 1

    edit.save("temp-edit.pdf", garbage = 4, deflate = True)
    shutil.move("temp-edit.pdf", toBeEditedPDFPath)
    rplcmnt.close()
    edit.close()
    
            












def main():    

    getAnnotatedPages(src, 0, 500)
    joinAndIndex(basePath + "//pages")
    indexed = parseTxt(basePath + "//indecies.txt")
    reinstate(basePath + "//total.pdf", basePath + "//Edit.pdf", indexed)
    pass

    

main()