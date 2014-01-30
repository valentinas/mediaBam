<html>
    <head>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script type="text/javascript" src="templates/js.js"></script>
        <link rel="stylesheet" type="text/css" href="templates/style.css"></link>
    </head>
    <body>
        <form action="/" method="get">
            {status}
            <p>
                Search: <input type="text" name="search">
                <br />
                <input type="submit" value="Submit">
            </p>
        </form>
        <table>
            <thead>
                <tr>
                    <td>Title</td>
                    <td>Details</td>
                    <td>Seeders</td>
                    <td>Leechers</td>
                    <td>Download to</td>
                </tr>
            </thead>
            <tbody>
                {searchResultsHTML}
            </tbody>
        </table>
    </body>
</html>
