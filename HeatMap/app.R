library(plotly)
library(shiny)

# compute a correlation matrix
sim.mat <- read.csv("C:/Users/ManaliT/Desktop/Semester 3/DV/Project/language_sim_matrix.csv", row.names=1)
Language_keywords <- read.csv("C:/Users/ManaliT/Desktop/Semester 3/DV/Project/Language_keywords.csv")
nms <- names(sim.mat)

ui <- fluidPage(
  mainPanel(
    plotlyOutput("heat"),  bubblesOutput("bubble")
  )
 #verbatimTextOutput("selection")
)

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
      common <- data.frame(rbind(lang1, lang2, make.row.names=FALSE))
      dup <- data.frame(name=common[which(duplicated(common$name)),]$name)
      #dup <- cbind(dup, data.frame(count=NA))
      if(nrow(dup)==0)
        bubbles(value = runif(26), label = LETTERS,
                color = rainbow(26, alpha=NULL)[sample(26)])
      else
      {
      dup$count <- sapply(dup$name, function(x){
        max(lang1[lang1$name==as.character(x),]$count, lang2[lang2$name==as.character(x),]$count)
      })
      
      bubbles::bubbles(value = dup$count, tooltip=dup$count,label = dup$name, color = rainbow(nrow(dup), alpha=NULL)[sample(nrow(dup))])
      } }
    
    else {
      bubbles(value = runif(26), label = LETTERS,
              color = rainbow(26, alpha=NULL)[sample(26)])
    }
  })
  
}
shinyApp(ui, server)