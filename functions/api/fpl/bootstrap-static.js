export async function onRequestGet() {
  return proxyFpl('https://fantasy.premierleague.com/api/bootstrap-static/');
}

async function proxyFpl(url) {
  try {
    const upstream = await fetch(url, { headers: { 'Accept': 'application/json' } });
    const headers = new Headers();
    headers.set('Content-Type', 'application/json; charset=utf-8');
    headers.set('Cache-Control', 'public, max-age=300, s-maxage=300');
    headers.set('X-Content-Type-Options', 'nosniff');
    return new Response(upstream.body, { status: upstream.status, headers });
  } catch (error) {
    return Response.json({ error: 'FPL upstream unavailable' }, { status: 502 });
  }
}
