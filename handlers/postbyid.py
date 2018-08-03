import webapp2
import time
import logging
from models import BlogModel, UserModel, CommentModel
import templater
from cookies import getUserFromRequest


class BlogHandler(webapp2.RequestHandler):
    # show the blog with the id
    def get(self, blog_id):
        post = BlogModel.get_by_id(int(blog_id))  # type: BlogModel
        if post:
            user = getUserFromRequest(self.request)  # type: UserModel
            userSignedIn = user is not None  # type: bool
            kwargs = {'post': post,
                      'userSignedIn': userSignedIn,
                      'current_user': user
                      }
            if user and post.author.key().id() == user.key().id():
                kwargs['showEdit'] = True
            self.response.write(
                templater.render_a_post(**kwargs)
            )
        else:
            self.response.write("blog entry not found")

    def post(self, blog_id):
        """
        This method is used to handle comment post/edit/delete on a post
        """
        user = getUserFromRequest(self.request)  # type: UserModel
        if user:
            post = BlogModel.get_by_id(long(blog_id))  # type: BlogModel
            if not post:
                # no post found. so redirect to default page.
                self.redirect('/blog/all')
                return
            logging.info(self.request)
            commentBtnAction = self.request.get('commentBtn')  # type:str
            # update/create a new comment
            if commentBtnAction:
                # check if the comment body is valid
                content = self.request.get('content')
                if content:
                    if commentBtnAction == 'comment':
                        # create comment
                        cmnt = CommentModel(author=user, post=post, content=content)
                        cmnt.put()
                        # making the page to refresh after putting content; because of db eng consistency problems
                        time.sleep(0.1)
                    elif commentBtnAction.isdigit():
                        # update comment by the id
                        cmnt = CommentModel.get_by_id(long(commentBtnAction))  # type: CommentModel
                        # confirm that the comment is updated by its author
                        if cmnt and user.key() == cmnt.author.key():
                            cmnt.content = content
                            cmnt.put()
                            time.sleep(0.1)
            # delete comment
            elif self.request.get('deleteComment'):
                commentId = self.request.get('deleteComment')  # type:str
                if commentId and commentId.isdigit():
                    cmnt = CommentModel.get_by_id(long(commentId))  # type: CommentModel
                    # confirm that the comment is deleted by its author
                    if cmnt and user.key() == cmnt.author.key():
                        logging.info('cmnt %s' % cmnt)
                        cmnt.delete()
                        time.sleep(0.1)
            # like or dislike posts
            elif user.key().id() != post.author.key().id():
                # author of the post can't like his own
                if self.request.get('likeComment'):
                    # add the like count if the user already didn't liked
                    if user.key().id() not in post.likes:
                        post.likes.append(user.key().id())
                        post.likescount = int(post.likescount) + 1
                        # persist changes
                        post.put()
                        time.sleep(0.1)
                elif self.request.get('dislikeComment'):
                    # reduce the like count and pop user id from list
                    if user.key().id() in post.likes:
                        post.likes.remove(user.key().id())
                        post.likescount = int(post.likescount) - 1
                        # persist changes
                        post.put()
                        time.sleep(0.1)

            self.redirect('/blog/%s' % blog_id)
        else:
            self.redirect('/signin')
