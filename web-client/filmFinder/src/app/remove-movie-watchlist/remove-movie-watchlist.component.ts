import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {UserMessageConstant} from '../constants/UserMessageConstant';
import {WebService} from '../services/web.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {WishlistRemove} from '../models/WishlistRemove';

@Component({
  selector: 'app-remove-movie-watchlist',
  templateUrl: './remove-movie-watchlist.component.html',
  styleUrls: ['./remove-movie-watchlist.component.css']
})
export class RemoveMovieWatchlistComponent implements OnInit {
  @Input() public movieID: number;
  snackbarDuration = 2000;
  @Output() deleteFromWatchlist = new EventEmitter<number>();
  constructor(private webService: WebService, private snackbar: MatSnackBar) { }

  ngOnInit(): void {
  }
  onClick(): void{
    this.webService.removeWatchlist(this.movieID).subscribe(success => {
      this.successfulUpdateSnackbar(UserMessageConstant.WATCHLIST_REMOVED, UserMessageConstant.DISMISS);
      this.deleteFromWatchlist.emit(this.movieID);
    }, err => {
      this.successfulUpdateSnackbar(UserMessageConstant.WATCHLIST_REMOVED_UNSUCCESSFUL, UserMessageConstant.DISMISS);
    });
  }

  private successfulUpdateSnackbar(message, action): void {
    const snackbarRef = this.snackbar.open(message, action, {duration: this.snackbarDuration});
    snackbarRef.afterDismissed().subscribe(() => {});
  }
}