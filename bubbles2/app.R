library(plotly)
library(shiny)
#devtools::install_github("jcheng5/bubbles")
library(bubbles)

# compute a correlation matrix
simmat <- read.csv("data/language_sim_matrix.csv", row.names=1)
sim <- as.matrix(simmat)

Language_keywords <- read.csv("data/Language_keywords.csv")
Language_keywords2 <- read.csv("data/language_common_topics.csv")

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
       if(as.character(s[["x"]])!=as.character(s[["y"]]))
      {  
        combo1 <- paste(as.character(tolower(s[["x"]])),"-",as.character(tolower(s[["y"]])), sep="")
        combolang1 <- Language_keywords2[Language_keywords2$language_pair==combo1,]
        combo2 <- paste(as.character(tolower(s[["y"]])),"-",as.character(tolower(s[["x"]])), sep="")
        combolang2 <- Language_keywords2[Language_keywords2$language_pair==combo2,]
        combolang <- data.frame(rbind(combolang1, combolang2, make.row.names=FALSE))
        yrPal <- colorRampPalette(c("#E0F7FA", "#00ACC1"))
        if(nrow(combolang)==0)
          bubbles(value = runif(26), label = LETTERS,
                  color = yrPal(26)[runif(26),breaks = 8])
        else
        {
          yrPal <- colorRampPalette(c("#E0F7FA", "#00ACC1"))
          combolang$color <- yrPal(10)[as.numeric(cut(combolang$count,breaks = 8))]
        bubbles::bubbles(value = combolang$count, tooltip=combolang$count,label = combolang$topic, color = combolang$color)
        }
      }
      else 
      {
        #Tags for each language
        lang <- Language_keywords[which(grepl(as.character(s[["x"]]), Language_keywords$Language, ignore.case = TRUE)),]
        yrPal <- colorRampPalette(c("#E0F7FA", "#00ACC1"))
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