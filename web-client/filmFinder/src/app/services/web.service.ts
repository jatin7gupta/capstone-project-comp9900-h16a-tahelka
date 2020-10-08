import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {AuthenticationService} from './authentication.service';
import {Observable} from 'rxjs';
import { User } from '../models/User';
import { NewUser } from '../models/NewUser';
import {Search} from '../models/Search';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})
export class WebService {
  API_URL =  'http://127.0.0.1:5000/api/v1/';
  constructor(private http: HttpClient, private authenticationService: AuthenticationService) { }
  login(user: User): Observable<any> {
    const loginUrl = this.API_URL + 'tokens';
    return this.http.post(loginUrl, user, httpOptions);
  }
  signup(user: NewUser): Observable<any> {
    const signupUrl = this.API_URL + 'users';
    return this.http.post(signupUrl, user, httpOptions);
  }
  search(searchObject: Search): Observable<any> {
    const moviesUrl = this.API_URL + 'movies';
    let headers = new HttpHeaders();
    headers = headers.set('Authorization', 'Bearer ' + this.authenticationService.currentUserValue.token);
    const params = new HttpParams()
      .set('name', searchObject.name)
      .set('abc', 'def');
    return this.http.get(moviesUrl, {params, headers});
  }
}