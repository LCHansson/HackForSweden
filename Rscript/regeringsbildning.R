## Libraries
require(stringr)

## Read data

testdata <- read.table(
  file = "data/valresultat/slutligt_valresultat_valdistrikt_R.skv",
  header = TRUE,
  sep = ";",
  nrows = 10,
  fileEncoding = "ISO8859-1",
  stringsAsFactors = FALSE
)



## Define algorithm
#' FIND MANDATES
#' After an election, we want to distribute parliamentary mandates based on a vote
#' share, but after considering some election threshold. In Sweden this threshold
#' is set to 4% of the popular vote.
#' 
#' The mandates are distributed by the Sainte-Laguë method ("jämkade uddatalsmetoden")
#' using 1.4 as initial divisor.

findSeats <- function(voteList, threshold = 4, seats = 349) {
  # Result strings need to be converted from Swedish to English decimal marker
  voteList = lapply(voteList, str_replace_all, ",", ".")
  
  # Only look at percentages
  partiResultNames = names(voteList)[str_detect(names(voteList), "proc")]
  voteList = voteList[names(voteList) %in% partiResultNames]
  
  # If the party recieved less than the threshold, its votes are excluded from the 
  # seat distribution algorithm
  partiResults = sapply(voteList, function(partiResult) {
    if (as.numeric(partiResult) < threshold)
      return(0)
    else
      return(as.numeric(partiResult))
  })
  names(partiResults) = sapply(names(partiResults), str_replace_all, ".proc", "")
  
  
  # The number of seats are distributed among the remaining parties using
  # Sainte-Laguë
  mandateList = list(S=0, V=0, MP=0, M=0, FP=0, KD=0, C=0, SD=0, FI=0, PP=0, SPI=0, OVR=0, BL=0, OG=0)
  
  for (i in 1:seats) {
    seatWinner = which.max(sapply(names(partiResults), function(parti) {
      result = partiResults[[parti]]/(1 + mandateList[[parti]])
      return(result)
    }))
    mandateList[names(seatWinner)] = mandateList[[names(seatWinner)]] + 1
  }
  
  return(mandateList)
}



#' FIND GOVERNMENT
#' The basic problem is this: Given a strength balance between political parties,
#' decide which potential party coalition might form a government.
#' 
#' The function takes a formatted list of 
#' 
#' We assume the following premises:
#' * All parties have a specified list of which parties they _can_ cooperate with
#' and which parties they _can't_ cooperate with.
#' * The biggest party in a coalition "selects" its coalition partners. Thus,
#' the biggest party will go first in trying to form a coalition. It then scans
#' for potential coalition partners and decides whether they can form a coalition
#' with them.
#' * If the biggest party fails at finding a coalition, the second biggest party
#' tries to do the same thing.
#' * If no party with a vote share above 20% manages to form a coalition, the 
#' coalition formation is considered to have failed.
#' * Parties stop looking for coalition partners once they have reached >50% of
#' the mandate share.

findGovernment <- function(mandateList) {
  
}





#' EXAMPLES
#' 
#' voteList = votesInMyDistrict
#' mandateList = findMandates(voteList)
#' 
#' government = findGovernment(mandateList)

