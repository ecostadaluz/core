%setdefault('title','')
%setdefault('playlist','')
%setdefault('playlistsize','')
<!doctype html>
<html class="no-js" lang="pt">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{{title}}</title>
        <link rel="stylesheet" href="/static/css/largefoundation.css" />
        <link rel="stylesheet" href="/static/css/gap.css" />
        <script src="/static/js/modernizr.js"></script>
    </head>
    <body>
        %print("aqui no espera playlist ----------------------------------------"+str(title))
        <div class="row">
            <div class="large-7 medium-8 columns">
                <br> <br>
                <div class="row">
                    <div class="large-6 columns">
                        <div class="panel">
                            <p class="frist">Serviço</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="panel">
                            <p class="frist">Senha</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="panel">
                            <p class="frist">Balcão</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="large-6 columns">
                        <div class="callout1 panel">
                            <p class="frist">Telemoveis</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">A12</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">01</p>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="large-6 columns" >
                        <div class="callout1 panel">
                            <p class="frist">Tablets</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">B07</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">02</p>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="large-6 columns">
                        <div class="callout1 panel">
                            <p class="frist">Acessórios</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">C15</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">03</p>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="large-6 columns">
                        <div class="callout1 panel">
                            <p class="frist">Assistência</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">D03</p>
                        </div>
                    </div>
                    <div class="large-3 columns" id="coluna">
                        <div class="callout2 panel">
                            <p class="second">04</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="large-5 columns">
                <br></br>
                <div class="flex-video widescreen vimeo">
                <video id="Videotv" width="520" height="500"  autoplay controls>
                </video>
                <img id="Imagetv" width="520" height="500">
            </div>
                 <!-- Player Controler helpers -->
                 <input  name="nextmultimedia"  id="nextmultimedia" type="hidden" value="0" ></input>
                 <input  name="playlistsize"  id="playlistsize" type="hidden" value="{{!playlistsize}}" ></input>
                 <input  name="playlist"  id="playlist" type="hidden" value="{{!playlist}}" ></input>
                 <input  name="currentTime"  id="currentTime" type="hidden" value="00:00:00" ></input>
                 <input  name="targetTime"  id="targetTime" type="hidden" value="00:00:00" ></input>
                 <!-- weather widget -->
                <a href="http://www.accuweather.com/pt/cv/praia/55657/weather-forecast/55657" class="aw-widget-legal">
                </a>
                <div  id="time_widget" class="aw-widget-current"  data-locationkey="" data-unit="c" data-language="pt" data-useip="true" data-uid="awcc1430244570514">
                        <script type="text/javascript" src="http://oap.accuweather.com/launch.js">
                        </script>
                </div>
            </div>
        </div>

        <footer class="row">

            <div class="large-12 columns">

                <br>
                <div  class="callout2 panel">
                     <marquee id="footermarquee"><p id="footermessage" style="display: inline"></p></marquee>
                </div>
            </div>
        </footer>
        <script src="/static/js/jquery.js"></script>
        <script src="/static/js/foundation.min.js"></script>
        <script src="/static/js/gap.js"></script>
        <script>
                $(document).foundation();
                //faz a busca pelo feed rss das noticias
                searchNews();
                //Controla a lista de reproduçao
                playerControler();
        </script>
    </body>
</html>
