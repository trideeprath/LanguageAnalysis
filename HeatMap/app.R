library(plotly)
library(shiny)
#devtools::install_github("jcheng5/bubbles")
library(bubbles)

# compute a correlation matrix
simmat <- read.csv("data/language_sim_matrix.csv", row.names=1)
sim <- as.matrix(simmat)

Language_keywords <- read.csv("data/Language_keywords.csv")
nms <- names(simmat)

ui <-  fluidPage(fluidRow(
  column(6,plotlyOutput("heat")),
  #column(6, verbatimTextOutput("title"), bubblesOutput("bubble"))
  column(6, bubblesOutput("bubble"))
))

server <- function(input, output, session) {
  output$heat <- renderPlotly({
    plot_ly(x=nms, y=nms, z=sim, key=sim, colors ="Blues", type = "heatmap") %>%
      layout(xaxis = list(title = ""), 
             yaxis = list(title = ""))
  })
  
  output$bubble <- bubbles::renderBubbles({
    s <- event_data("plotly_click")
    if (length(s)) {
      vars <- c(s[["x"]], s[["y"]]) # s[["x"]] and s[["y"]] are lang1 and lang2
      library(bubbles)
      lang1 <- Language_keywords[which(grepl(as.character(s[["x"]]), Language_keywords$Language, ignore.case = TRUE)),]
      lang2 <- Language_keywords[which(grepl(as.character(s[["y"]]), Language_keywords$Language, ignore.case = TRUE)),]
      if(as.character(s[["x"]])!=as.character(s[["y"]]))
      {  
      common <- data.frame(rbind(lang1, lang2, make.row.names=FALSE))
      dup <- data.frame(name=common[which(duplicated(common$name)),]$name)
     
      if(nrow(dup)==0)
        bubbles(value = runif(26), label = LETTERS,
                color = rainbow(26, alpha=NULL)[sample(26)])
      else
      {
      dup$count <- sapply(dup$name, function(x){
        max(lang1[lang1$name==as.character(x),]$count, lang2[lang2$name==as.character(x),]$count)
      })
      yrPal <- colorRampPalette(c('yellow', 'red'))
      dup$color <- yrPal(10)[as.numeric(cut(dup$count,breaks = 10))]

      #bubbles::bubbles(value = dup$count, tooltip=dup$count,label = dup$name, color = heat.colors(nrow(dup), alpha = NULL)[sample(nrow(dup))])
      bubbles::bubbles(value = dup$count, tooltip=dup$count,label = dup$name, color = dup$color)
      }
      }
      else 
      {
        #Tags for each language
        
        lang <- Language_keywords[which(grepl(as.character(s[["x"]]), Language_keywords$Language, ignore.case = TRUE)),]
        yrPal <- colorRampPalette(c('yellow', 'red'))
        lang$color <- yrPal(10)[as.numeric(cut(lang$count,breaks = 10))]
        bubbles::bubbles(value = lang$count, tooltip=lang$count,label = lang$name, color = lang$color)
        
        }  
      
      }
    
    else {
      bubbles(value = runif(26), label = LETTERS,
              color = heat.colors(26, alpha=NULL)[sample(26)])
    }
  })
  
  output$title <- renderPrint({
    
    s <- event_data("plotly_click")
    if (is.null(s)) "Click on a Similarity Matrix cell!" else
    {
      if(s[["x"]]==s[["y"]])
        paste("Top tags for ", trimws(s[["x"]]))
      else
      paste("Common tags between ", s[["x"]], " and ", s[["y"]])
      
    }
  })
   

   
}
shinyApp(ui, server)