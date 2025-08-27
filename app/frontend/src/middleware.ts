/********************** Modules **********************/
import { NextRequest, NextResponse } from 'next/server'

// Settings
import { settings } from '@/helpers/settings';

// Routes
import { routes } from './helpers/routes';

// Auth
import { useAuth } from "@/context/auth";

/********************** Variables **********************/
const protectedRoutes = [
  routes.auth.logout, routes.account.home, routes.channel.opts.create,
];
const protectedRoutesPre = [
  "studio"
];
const publicRoutes = [routes.auth.signin, routes.auth.signup];

/********************** Function **********************/
export default async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;

  const isProtectedRoute = protectedRoutes.includes(path);
  const isPublicRoute = publicRoutes.includes(path);

  const token = req.cookies.get(settings.token_name)?.value;

  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL(routes.auth.signin, req.nextUrl));
  }

  if (protectedRoutesPre.some(route => path.startsWith(`/${route}`)) && !token) {
    return NextResponse.redirect(new URL(routes.auth.signin, req.nextUrl));
  }

  if (isPublicRoute && token) {
    return NextResponse.redirect(new URL(routes.public.home, req.nextUrl));
  }

  return NextResponse.next();
}

/********************** Config **********************/
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
