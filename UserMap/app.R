library(shiny)
library(leaflet)

choices <- c("Java", "MySQL", "C", "C++", "Python", "SQL", "JavaSript", "HTML", "MATLAB", "Swift")
mapdata <- read.csv("data/aggregated_mapdata.csv")
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
  lang2markers <- mapdata[mapdata$Language==as.character(tolower(trimws(input$val2))),]
    
clusOptions1 = markerClusterOptions(iconCreateFunction=JS("function (cluster) {    
    var childCount = cluster.getChildCount();  
                                                              if (childCount < 300) {  
                                                              c = 'rgba(179, 201, 217, 0.7);'
                                                              } else if (childCount < 600) {  
                                                              c = 'rgba(72, 158, 186, 0.7);'  
                                                              } else { 
                                                              c = 'rgba(22, 83, 110, 0.7);'  
                                                              }    
                                                              return new L.DivIcon({ html: '<div style=\"background-color:'+c+'\"><span>' + childCount + '</span></div>', className: 'marker-cluster', iconSize: new L.Point(40, 40) });
                                                              
  }"))
    clusOptions2 = markerClusterOptions(iconCreateFunction=JS("function (cluster) {    
                                                              var childCount = cluster.getChildCount();  
                                                              if (childCount < 300) {  
                                                              c = 'rgba(254, 208, 122, 0.7);'
                                                              } else if (childCount < 600) {  
                                                              c = 'rgba(254, 135, 37, 0.7);'  
                                                              } else { 
                                                              c = 'rgba(207, 59, 2, 0.7);'  
                                                              }    
                                                              return new L.DivIcon({ html: '<div style=\"background-color:'+c+'\"><span>' + childCount + '</span></div>', className: 'marker-cluster', iconSize: new L.Point(40, 40) });
                                                              
    }"))

    leaflet() %>% 
    addTiles() %>% 
    addCircleMarkers(lng= lang1markers$Longitude, lat= lang1markers$Latitude, clusterOptions = clusOptions1, color="Blue") %>% 
    addCircleMarkers(lng= lang2markers$Longitude, lat= lang2markers$Latitude, clusterOptions = clusOptions2, color="Red") %>%
    addLegend(colors=c("#b3c9d9","#489eba", "#16536e"), labels=c("<300", ">300 & <600", ">600"), title=paste(input$val1, " Users"))%>%
    addLegend(colors=c("#fed07a","#fe8725", "#cf3b02"), labels=c("<300", ">300 & <600", ">600"), title=paste(input$val2, " Users"))
    })
}

shinyApp(ui=ui, server = server)