
#project ideas 
# 1. Show the geographical distribution of posts for every language 
# 2. Show some network visualizations (like how languages are inter-related)

require(wordcloud)
require(shiny)
require(shinyBS)
require(googleVis)
require(devtools)
install_github("jcheng5/bubbles", force=TRUE)

question_keyphrases <- read.csv("../data/question_keyphrases.csv")

ui <- fluidPage( tabsetPanel(
  tabPanel("Home", 
           actionLink("javalink", "Java"),
           bsModal("javapopup", "Popular topics in Java", "javalink", size = "large"),
           bubbles::bubblesOutput("javaBubble")),
  tabPanel("User Analysis", "contents"),
  tabPanel("Compare Languages", "contents")))


server <- function(input, output, session) {
  observeEvent(input$javalink, { output$javaBubble <- bubbles::renderBubbles({
     set.seed(20)
     java <- question_keyphrases[question_keyphrases$language=="java",]
     bubbles::bubbles(value = java$tfidf*10, label = java$keyphrase,
                      color = palette(topo.colors(30)))
   }) })
#  observeEvent(input$javalink, {
#    session$sendCustomMessage(type = 'testmessage',
#                              message = 'Thank you for clicking')
#  } )
}


shinyApp(ui = ui, server = server)