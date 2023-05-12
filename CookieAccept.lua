function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  local cookieAccept = splash:select("#cmpbntyestxt")
  assert(cookieAccept:mouse_click())
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end