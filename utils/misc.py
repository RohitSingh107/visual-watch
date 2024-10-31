
def expand_genre(genre: str):
    match genre:
        case "drm":
            return "Drama"
        case "trl":
            return "Mystry & Thriller"
        case "cmy":
            return "Comedy"
        case "rma":
            return "Romance"
        case "act":
            return "Action"
        case "crm":
            return "Crime"
        case "scf":
            return "Science-Fiction"
        case "hrr":
            return "Horror"
        case "eur":
            return "Made in Europe"
        case "fnt":
            return "Fantasy"
        case "hst":
            return "History"
        case "doc":
            return "Documentary"
        case "war":
            return "War & Military"
        case "msc":
            return "Music"
        case "wsn":
            return "Western"
        case "fml":
            return "Family"
        case "rly":
            return "Reality TV"
        case "spt":
            return "Sport"
        case "ani":
            return "Animation"
        case _:
            return genre
