(function () {
  var elem = document.getElementById('text-to-annotate'),
            annotator = new Annotator(elem);

  var oldAuth = new Annotator.Plugin.AnnotateItPermissions().options.userAuthorize;

  annotator.setupPlugins({
    storeUrl: OpenText.Annotator.store,
    tokenUrl: "/__authtoken__"
  }, {
    Store: {
      loadFromSearch: { limit: 1000 }
    },
    Permissions: false,
    AnnotateItPermissions: {
      userString: function (user) {
        if (typeof user === 'string') {
          return user;
        } else if (user.hasOwnProperty('name') && typeof user.name === 'string') {
          return user.name;
        } else if (user.hasOwnProperty('id') && typeof user.id === 'string') {
          return user.id;
        }
      },
      userAuthorize: function (action, annotation, user, consumer) {
        if (typeof user === 'string') {
          return oldAuth.call(this, action, annotation, user, consumer);
        } else if (user.hasOwnProperty('id') && typeof user.id === 'string') {
          return oldAuth.call(this, action, annotation, user.id, consumer);
        }
      }
    }
  });
}());
        

