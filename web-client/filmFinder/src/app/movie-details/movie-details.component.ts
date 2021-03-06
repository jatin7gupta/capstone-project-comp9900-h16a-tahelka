import {Component, Input, OnInit, Output} from '@angular/core';
import {MovieResult} from '../models/MovieResult';
import {WebService} from '../services/web.service';
import {Search} from '../models/Search';
import {MovieDetails} from '../models/MovieDetails';
import { EventEmitter } from '@angular/core';
import {Recommendations} from '../models/Recommendations';
import {MovieReview} from '../models/MovieReview';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  @Input() movie: MovieResult;
  movieDetailsObject: MovieDetails;
  displayedColumns: string[] = ['title', 'year', 'rating', 'description', 'genre', 'director', 'cast'];
  dataSource: MovieDetails[];
  @Output() reviews = new EventEmitter<MovieReview[]>();
  constructor(private webService: WebService) { }

  ngOnInit(): void {
  }
  // http call for movie detail
  movieDetails(): void {
      this.webService.movieDetails(this.movie.movieID).subscribe(success => {
        this.movieDetailsObject = success;
        this.dataSource = [success];
        // tell parent that movie has been reviewed
        this.emitMovieReviews(this.movieDetailsObject.reviews);
      }, err => {
        alert(JSON.stringify(err));
      });
    }
  emitMovieReviews(movieReviews: MovieReview[]): void {
    this.reviews.emit(movieReviews);
  }
}
