sourceBiocinstallScript <- function()
{
    ## Make sure we didn't get here by mistake 
    ## e.g.(old biocLite function stored in global environment).
    vers <- getRversion()
    biocVers <-
        tryCatch(tools:::.BioC_version_associated_with_R_version,
                 error=function(...) numeric_version(0.0))
    
    stopifnot(require("utils"))
    REQUIRED_R_VERSION <- "2.1.0"
    CURRENT_R_DEVEL_VERSION <- "2.14.0"
    ## Verify we're running a recent enough version of R.
    thisRVer <- paste(R.Version()[c("major", "minor")], collapse=".")
    if (compareVersion(thisRVer, REQUIRED_R_VERSION) < 0) {
        ## R versions less than 2.1.0 need to use the old (BioC 1.5) version
        ## of getBioC.R
        stop("Your R version is ", thisRVer, ".\n",
             "Bioconductor requires an R version greater than ",
             REQUIRED_R_VERSION, ".\n",
             "To obtain the latest version of R, please see:\n",
             "  http://www.r-project.org/\n")
    }
    chopRVer <- function(RVer) gsub("(\\w+).(\\w+).(\\w+)", "\\1.\\2", RVer)
    if (compareVersion(thisRVer, CURRENT_R_DEVEL_VERSION) >= 0) {
        choppedRVer <- chopRVer(CURRENT_R_DEVEL_VERSION)
    } else {
        choppedRVer <- chopRVer(thisRVer)
    }
    scriptUrl <- paste("http://bioconductor.org",
                       "installScripts",
                       choppedRVer,
                       "biocinstall.R", sep="/")
    if (vers > "2.13" && biocVers > "2.8") {
        scriptUrl <- "http://bioconductor.org/fixBiocLite.R"
    }
    
    ## Don't add any arg to the safeSource() function and don't define any local
    ## variable in it. This is the only way to make sure the call to ls() only
    ## returns the list of symbols that result from the call to source().
    safeSource <- function()
    {
        source(scriptUrl, local=TRUE)
        for (objname in ls(all.names=TRUE)) {
            if (exists(objname, envir=.GlobalEnv, inherits=FALSE))
                warning("Redefining ", sQuote(objname))
            .GlobalEnv[[objname]] <- get(objname, inherits=FALSE)
        }
    }
    safeSource()
}

sourceBiocinstallScript()

### Install Bioconductor packages using CRAN-style repositories.
### ...: arguments passed to install.packages.
getBioC <- function(...) biocinstall(...)
