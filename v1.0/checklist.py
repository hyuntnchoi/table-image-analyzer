import cv2

def init(imagePath):
    print('=== [START] IMAGE READING ===')
    global img
    global rows, cols, channels
    global entireHeight, entireWidth
    global checklistHeight, checklistWidth
    global startX, startY
    global endX, endY
    global rowList, rowHeight, rowColumnList, columnWidthList
    
    print('img:', imagePath)
    img = cv2.imread(imagePath)

    rows,cols,channels = img.shape

    entireHeight = img.shape[0]
    entireWidth = img.shape[1]
    checklistHeight = 0
    checklistWidth = 0
    startX = 0
    startY = 0
    endX = 0
    endY = 0
    rowList = []
    rowHeight = []
    rowColumnList = []
    columnWidthList = []

    print('>> Entire Height: ', entireHeight) 
    print('>> Entire Width: ', entireWidth)

    print('=== [END] IMAGE READING ===')

def getStartPx():
    print('=== [START] GETTING START PIXEL ===')
    
    global rows
    global cols

    for i in range(rows):
        for j in range(cols):
            px = img[i,j]
            if all(px < [200,200,200]):
                nextPx = img[i+1,j]
                if all(nextPx < [200,200,200]):
                    global startX
                    global startY
                    startY = i
                    startX = j
                    print('>> Start X : ', startX)
                    print('>> Start Y : ', startY)
                    return
 
    print('=== [END] GETTING START PIXEL ===')

def getRows():
    print('=== [START] GETTING ROWS ===')
    rowCnt = 0
    global startY
    global rowList
    y = startY
    rowList = []
    
    while y <= rows:
        nPx = img[y, startX+1]
        nnPx = img[y, startX+2]
        nnnPx = img[y, startX+3]
        nnnnPx = img[y, startX+4]
        if all(nPx < [200,200,200]) and all(nnPx < [200,200,200]) and all(nnnPx < [200,200,200]) and all(nnnnPx < [200,200,200]):
            print('>> Row detected')
            rowList.append([startX, y])
            #print(rowList)
            y = y + 3
        else:
            y += 1
        if y == rows-1:
            print('>> Created row count: ', len(rowList))
            break
    print('=== [END] GETTING ROWS ===')

def setEndY():
    print('=== [START] END Y SETTING ===')
    
    global endY
    
    if len(rowList) > 0:
        endY = rowList[-1][1]
        print('>> End Y :', endY)
    else:
        print('>> RowList is empty')
        print('>> End Y setting failed')
    
    print('=== [END] End Y setting ===')

def getChecklistHeight():
    print('=== [START] CHECKLIST ENTIRE HEIGHT SETTING ===')
    
    global checklistHeight
    global endY

    checklistHeight = endY-startY
    
    print('>> Checklist Height :', checklistHeight)
    print('=== [END] CHECKLIST ENTIRE HEIGHT SETTING ===')

def getChecklistWidth(): 
    print('=== [START] CHECKLIST ENTIRE WIDTH SETTING ===')
    
    global endX
    global startX
    global checklistWidth
    x = startX
    y = startY

    while x <= cols:
        x += 1
        curPx = img[y, x]
        nextPx = img[y, x+1]
        
        #if next pixel is white,
        #check below pixels of current pixel
        #and if the pixels are black
        #current pixel is last pixel of entire row
        if all(nextPx > [200,200,200]):
            bPx = img[y+1, x]
            bbPx = img[y+2, x]
            bbbPx = img[y+3, x]
            bbbbPx = img[y+4, x]
            if all(bPx < [200,200,200]) and all(bbPx < [200,200,200]) and all(bbbPx < [200,200,200]) and all(bbbbPx < [200,200,200]):
                endX = x
                checklistWidth = endX - startX
                print('>> End X: ', endX)
                print('>> Checklist Width :', checklistWidth)
                break
    
    if endX == 0: 
        print('>> Failed to set checklist width')
    print('=== [END] CHECKLIST ENTIRE WIDTH SETTING ===')


def getRatioBetweenRows():
    print('=== [START] CHECKLIST HEIGHT RATIO BTW ROWS ===')
    
    i = 0
    global rowHeight
    rowHeight = []

    for row in rowList:
        if len(rowList)-1 == i:
            height = 0
            rowHeight.append(height)
            break
        else:
            y1 = rowList[i][1]
            y2 = rowList[i+1][1]
            height = y2 - y1
            rowHeight.append(height)
        
        i += 1
    
    print('>> Row Height:', rowHeight)
    print('=== [END] CHECKLIST HEIGHT RATIO BTW ROWS ===')

def getRowColumns(row):
    print('=== [START] GETTING ROW COLUMNS ===')    
    
    global endX
    global rowColumnList
    tempList = []
    x = row[0]+2 #as 2 pixels usually used in starting point
    y = row[1]

    tempList.append(x) #insert start x in list 

    while x < endX:
        x += 1
        
        curPx = img[y, x]
        bPx = img[y+1, x]
        bbPx = img[y+2, x]
        bbbPx = img[y+3, x]
        
        if all(bPx < [200,200,200]):
            if all(bbPx < [200,200,200]):
                if all(bbbPx < [200,200,200]):
                    tempList.append(x)
                    x += 2
    
    rowColumnList.append(tempList)
    print('>> rowColumnList :', rowColumnList)

    print('=== [END] GETTING ROW COLUMNS ===')    

def getColumnWidth(row):  
    print('=== [START] GETTING COLUMN WIDTH ===')
    print(row)  
    global columnWidthList
    tempList = []
    i = 0
    
    while i < len(row) - 1:
        width = row[i+1] - row[i]
        tempList.append(width)
        i += 1

    columnWidthList.append(tempList)
    print('>> columnWidthList :', columnWidthList)

    print('=== [END] GETTING COLUMN WIDTH ===')

def main():
    print('>>ENTER IMAGE PATH:')
    img = input()
    init(img);
    getStartPx();
    getRows();
    setEndY();
    getChecklistHeight();
    getChecklistWidth();
    getRatioBetweenRows();

    for row in rowList:
        getRowColumns(row);

    for row in rowColumnList:
        getColumnWidth(row);

    print('=====================================')
    print('===SUCCESSFULLY ANALIZED THE IMAGE===')
    print('=====================================')
    
    print('>>ENTIRE WIDTH:', entireWidth)
    print('>>ENTIRE HEIGHT:', entireHeight)
    print('>>CHECKLIST WIDTH:', checklistWidth)
    print('>>CHECKLIST HEIGHT:', checklistHeight)
    print('>>STARTING PIXEL: [',startX,',',startY,']')
    print('>>ROW COUNT:', len(rowList))
    print('>>HEIGHT BTW ROWS:')
    i = 1
    for row in rowHeight:
        if i < len(rowHeight):
            print('row',i+1,' - row',i,': ',row,'px')
            i += 1
    
    print('>>COLUMNS WIDTH IN EACH ROW:')
    j = 1
    for row in columnWidthList:
        if j < len(columnWidthList):
            print('row',j,' columns width:',row)
            j += 1

main();
    
k = input('press close to exit')
