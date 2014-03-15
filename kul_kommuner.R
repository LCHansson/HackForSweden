districtsWithSD <- geoData$features[sapply(geoData$features, function(i) "SD" %in% names(unlist(i$properties$government$unnamedMinisters)))]

sapply(districtsWithSD, function(i) i$properties$VDNAMN)
## Distrikt med SD:
# Hållnäs: Tierpsvägen 14


districtsWithSPI <- geoData$features[sapply(geoData$features, function(i) "SPI" %in% names(unlist(i$properties$government$unnamedMinisters)))]

sapply(districtsWithSPI, function(i) i$properties$VDNAMN)
## Distrikt med SPI:
# Inga


districtsWithFI <- geoData$features[sapply(geoData$features, function(i) "FI" %in% names(unlist(i$properties$government$unnamedMinisters)))]

sapply(districtsWithFI, function(i) i$properties$VDNAMN)
## Distrikt med FI:
# Inga


districtsWithV <- geoData$features[sapply(geoData$features, function(i) "V" %in% names(unlist(i$properties$government$unnamedMinisters)))]

sapply(districtsWithV, function(i) i$properties$VDNAMN)
## Distrikt med V:
# 


districtsWithMP <- geoData$features[sapply(geoData$features, function(i) "MP" %in% names(unlist(i$properties$government$unnamedMinisters)))]

sapply(districtsWithMP, function(i) i$properties$VDNAMN)
## Distrikt med MP:
# 

districtsWithKD <- geoData$features[sapply(geoData$features, function(i) "KD" %in% names(unlist(i$properties$government$unnamedMinisters)))]

sapply(districtsWithKD, function(i) i$properties$VDNAMN)
## Distrikt med KD:
# 





oddDistricts <- list()
for (i in 1:length(geoData$features)) {
  biggestParty = names(which.max(sapply(geoData$features[[i]]$properties$government$unnamedMinisters, function(i) unlist(i))))
  if (!biggestParty %in% c("S","M"))
    oddDistricts <- append(oddDistricts, list(list(
      parti = biggestParty,
      distriktkod = geoData$features[[i]]$properties$LKFV,
      namn = geoData$features[[i]]$properties$VDNAMN
    )))
}

writeLines(toJSON(oddDistricts), "app/data/oddDistricts.json")




