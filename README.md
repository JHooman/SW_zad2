# SW_zad2
wykonanie skanu obrazu przez docker scout lub trivy zwraca 1 (true) jeżeli zostanie wykryte zagrożenie bezpieczeństwa poziomu  Wysokiego lub Krytycznego.
Ze względu na występowanie zagrożenia poziomu wysokiego w stowrzonej aplikacji wykonanie oby dwóch workflow nie pozwala na wysłanie obrazu do repozytorium ghcr.
2 ostatnie wykonania workflow są z załączonym zabezpieczeniem, a poprzednie dwa udane bez zabezpieczenia.


Fragment odpowiadający za skan w docker scout i wysłanie obrazu do repozytorium
```sh
      - name: Docker Scout
        id: docker-scout
        uses: docker/scout-action@v1
        with:
          command: cves,recommendations, sbom
          to-latest: false
          ignore-base: true
          ignore-unchanged: true
          only-fixed: true
          only-severities: critical,high
          exit-code: true
      - name: Push Docker Image
        if: success()
        run: |
          docker buildx imagetools create --tag ghcr.io/${{ vars.GH_USERNAME }}/sw_zad2_scout:latest  ${{ env.IMAGE_TAG }}

```

Fragment odpowiadający za skan w trivy i wysłanie obrazu do repozytorium
```sh
      - name: Scan with trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.IMAGE_TAG }}
          severity: CRITICAL,HIGH
          ignore-unfixed: true
          exit-code: 1
          format: table
      - name: Push Docker Image
        if: success()
        run: |
          docker buildx imagetools create --tag ghcr.io/${{ vars.GH_USERNAME }}/sw_zad2_trivy:latest  ${{ env.IMAGE_TAG }}
```

Adres repozytorium ghcr
http://ghcr.io/jhooman/sw_zad2_scout
http://ghcr.io/jhooman/sw_zad2_trivy
