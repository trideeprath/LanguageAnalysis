library(shiny)
library(leaflet)

choices <- c("Java", "MySQL", "C", "C++", "Python", "SQL", "JavaSript", "HTML", "MATLAB", "Swift")
mapdata <- read.csv("C:/Users/ManaliT/Desktop/Semester 3/DV/Project/UserMap/aggregated_mapdata.csv")
ui <- fluidPage(
  titlePanel("Select a language to explore user location densities"),
  fluidRow(column(2,
   selectInput("val1", choices = choices, label = "Language 1",  selected = "Java" ),
   selectInput("val2", choices = choices, label="Language 2", selected = "C++")),
  column(10,
    leafletOutput("map") 
    )                              
  )
)

server <- function(input, output, session){
  # Create the map
  output$map <- renderLeaflet({
    lang1markers <- mapdata[mapdata$Language==as.character(tolower(trimws(input$val1))),]
    leaflet(data=lang1markers) %>% addTiles() %>% addCircleMarkers(~Longitude, ~Latitude, clusterOptions = markerClusterOptions(), color="Blue")
    lang2markers <- mapdata[mapdata$Language==as.character(tolower(trimws(input$val2))),]
    leaflet(data=lang1markers) %>% addTiles() %>% addCircleMarkers(~Longitude, ~Latitude, clusterOptions = markerClusterOptions(), color="Blue")
    
    })
}

shinyApp(ui=ui, server = server)