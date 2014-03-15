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
#' share, but after cosidering some election threshold. In Sweden this threshold
#' is set to 4% of the popular vote.

findMandates <- function(voteList, threshold = 4) {
  # Result strings need to be converted from Swedish to English decimal marker
  voteList = lapply(voteList, str_replace_all, ",", ".")
  
  # Only look at percentages
  partiResultNames = names(voteList)[str_detect(names(voteList), "proc")]
  voteList = voteList[names(voteList) %in% partiResultNames]
  
  # If the party recieved less than the threshold
  partiResults = lapply(voteList, function(partiResult) {
    if (as.numeric(partiResult) < threshold)
      return(0)
    else
      return(as.numeric(partiResult))
  })
}



#' FIND GOVERNMENT
#' The basic problem is this: Given a strength balance between political parties,
#' decide which potential party coalition might form a government.
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

